from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM, TextIteratorStreamer
from IPython.core.magic import register_line_magic, register_cell_magic, register_line_cell_magic
from IPython.display import display, Markdown, clear_output
from IPython import get_ipython
import torch
import pandas as pd
import ast
import numpy as np
from threading import Thread
import time
from rank_bm25 import BM25Okapi
import nltk
from nltk.tokenize import word_tokenize
from huggingface_hub import login
import random
import ipywidgets as widgets
import json

from langchain_openai import OpenAI, ChatOpenAI

# Necessary so that query embedding match (initialization) the pre-computed corpus embeddings
torch.manual_seed(0)
np.random.seed(0)

#########################################################################################################################################

class UPSayAI:
    def __init__(self, model_name="aristote/llama", model_api_key=None, model_temperature=0.7, model_max_tokens=1024, rag_model="dpr", rag_min_relevance=0.5, rag_max_results=5, recommendation_min_relevance=0.7, quiz_min_relevance=0.2, quiz_max_results=100, num_questions_quiz=5, course_corpus_file="corpus_ISD.csv"):
        self.model_name = model_name
        self.model_api_key = model_api_key
        self.model_temperature = model_temperature
        self.model_max_tokens = model_max_tokens
        self.rag_model = rag_model
        self.rag_min_relevance = rag_min_relevance
        self.rag_max_results = rag_max_results
        self.recommendation_min_relevance = recommendation_min_relevance
        self.quiz_min_relevance = quiz_min_relevance
        self.quiz_max_results = quiz_max_results
        self.course_corpus_file = course_corpus_file
        self.num_questions_quiz = num_questions_quiz
        
        self.config_rag()

        self.config_llm()
        self.selected_answers = [None, None, None, None, None]

        self.setup_magics()


    def config_rag(self):
        if self.rag_model == "dpr":
            self.load_corpus_embeddings()
            self.config_query_embedding()
        elif self.rag_model == "bm25":
            self.config_bm25()
        else:
            raise ValueError("Invalid rag_model. Current supported values are 'dpr' or 'bm25'")   

    def config_llm(self):
        if self.model_name == "aristote/llama" or self.model_name == "aristote/mixtral":
            self.config_llm_aristote()
        elif self.model_name == "huggingface/llama":
            self.config_llm_huggingface()
        else:
            raise ValueError("Invalid model_name. Current supported values are 'aristote/llama', 'aristote/mixtral', or 'huggingface/llama'")
            
        # Configure prompts for the LLMs
        # QR (for %ai_question)
        self.persona_prompt_qa = "Vous êtes un assistant virtuel qui aide les étudiants de l'Université Paris-Saclay avec des questions dans le domaine de la programmation et de la science des données, en répondant toujours de manière pédagogique et polie. Lorsque c'est possible, essayez d'utiliser des informations et des exemples tirés du matériel de cours pour aider l'étudiant à comprendre, en soulignant dans votre explication où l'étudiant a vu ce contenu être employé pendant le cours et en mettant toujours en contexte pour une réponse bien structurée."
        self.messages_history = []
        
        # Code generation (for %ai_code)
        self.persona_prompt_code = "Vous êtes un assistant virtuel qui écrit des codes python selon les instructions d'un étudiant de l'Université Paris-Saclay. Utilisez toujours des commentaires et documentez bien vos codes pour les rendre faciles à comprendre pour l'étudiant. Mettez toujours tout le code, y compris les éventuels exemples pratiques d'utilisation, dans un seul bloc délimité par '```python' au début et '```' à la fin. Ne générez pas plus d'un bloc de code, générez toujours un seul bloc avec tout le code et les exemples d'utilisation à l'intérieur afin que l'étudiant puisse tout exécuter dans une seule cellule jupyter. Utilisez des bibliothèques et des fonctions avec lesquelles l'étudiant est plus susceptible d'être familier, donnez la préférence à des solutions plus simples tant qu'elles sont correctes et entièrement fonctionnelles. Assurez-vous que votre code est correct, fonctionnel et que les éventuels exemples d'utilisation fonctionneront parfaitement et donneront des résultats corrects lorsqu'ils seront exécutés par l'étudiant. Terminez toujours par un court paragraphe après le bloc de code python (délimité par '```python' au début et '```') avec une description textuelle et des explications pour l'étudiant afin d'améliorer sa compréhension du sujet et du code généré."

        # Quiz (for %ai_quiz)
        self.quiz_subject = ""
        self.persona_prompt_quiz = f"Vous êtes un générateur de quiz style QCM pour des étudiants de niveau débutant qui souhaitent tester leurs connaissances dans le cadre de leurs études et de leur préparation aux examens. Générez 5 questions en français style QCM de niveau débutant sur le cours {self.quiz_subject} qui vous sera donnée par l'étudiant, où chaque question n'a qu'une seule réponse correcte et trois réponses incorrectes. Basez vos questions principalement sur les contenus liés aux mathématiques et à la programmation vus par l'étudiant pendant le cours, mais n'hésitez pas à poser des questions sur le même sujet concernant des détails qui n'apparaissent pas explicitement dans le cours mais que l'étudiant devrait connaître, à condition qu'elles soient pertinentes et au même niveau de difficulté." + """ Organisez les questions générées dans une liste de dictionnaires en python, où chaque dictionnaire représente une question formatée comme suit : [{"énoncé": "Question à l'élève (1) ?", "bonne_réponse": "Ceci est la réponse correcte à la question 1.", "mauvaises_réponses":["Ceci est la première réponse incorrecte à la question 1.", "Ceci est la deuxième réponse incorrecte à la question 1.", "Ceci est la troisième réponse incorrecte à la question 1."]}, ...]. N'oubliez pas de séparer les éléments des dictionnaires et de la liste par des virgules. Ne retournez rien d'autre que la liste des dictionnaires dans le bon format avec les questions QCM en français sur le sujet mentionné."""
        

    # Load corpus contents and embeddings
    def load_corpus_embeddings(self):
        try:
            self.df = pd.read_csv(self.course_corpus_file)
        except:
            raise ValueError("Course corpus file file not found.")
        try:
            self.df['embeddings'] = self.df['embeddings'].apply(ast.literal_eval)
            self.df['embeddings'] = self.df['embeddings'].apply(lambda x: torch.from_numpy(np.array(x)))
            self.df = self.df[self.df["content"].apply(lambda x: isinstance(x, str))].reset_index(drop=True)
            self.corpus_embeddings = self.df["embeddings"].tolist()
            self.corpus_embeddings = torch.stack([doc for doc in self.corpus_embeddings])
            self.corpus_embeddings = self.corpus_embeddings.float()
        except:
            raise ValueError("Course corpus file does not contain expected columns")

    # Query embedding tokenizer and model from HuggingFace. Only called if rag_model="dpr". 
    def config_query_embedding(self):
        self.tokenizer_dpr = AutoTokenizer.from_pretrained("etalab-ia/dpr-question_encoder-fr_qa-camembert",  do_lower_case=True, resume_download=None)
        self.model_dpr = AutoModel.from_pretrained("etalab-ia/dpr-question_encoder-fr_qa-camembert", return_dict=True, resume_download=None)

    # Confif BM25 retrieval
    def config_bm25(self):
        try:
            self.df = pd.read_csv(self.course_corpus_file)
            self.df = self.df[self.df["content"].apply(lambda x: isinstance(x, str))].reset_index(drop=True)
        except:
            raise ValueError("Course corpus file file not found.")
        try:
            self.bm25_index = BM25Okapi(self.df.tokenized_content.tolist())
        except:
            raise ValueError("Course corpus file does not contain expected columns")
    
    # Config LLM for aristote models
    def config_llm_aristote(self):
        if self.model_name == "aristote/llama":
            self.model = ChatOpenAI(openai_api_base = "https://dispatcher.aristote.centralesupelec.fr/v1", openai_api_key = self.model_api_key, model = "casperhansen/llama-3-70b-instruct-awq", temperature=self.model_temperature, max_tokens=self.model_max_tokens)
        elif self.model_name == "aristote/mixtral":
            self.model = ChatOpenAI(openai_api_base = "https://dispatcher.aristote.centralesupelec.fr/v1", openai_api_key = self.model_api_key, model = "casperhansen/mixtral-instruct-awq", temperature=self.model_temperature, max_tokens=self.model_max_tokens)

    # Config LLM for huggingface models (currently only Meta-Llama-3-8B-Instruct)
    def config_llm_huggingface(self):
        login(token=self.model_api_key)
        model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
                    model_id,
                    torch_dtype=torch.bfloat16
                )
        
        self.model.to(self.device)
        
        self.terminators = [
                        self.tokenizer.eos_token_id,
                        self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
                    ]
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        # Configure streamer for token-by-token display
        self.streamer = TextIteratorStreamer(self.tokenizer, skip_prompt = True)

    
        
    # Function to compute query embedding from the raw text (string)
    def get_query_embedding(self, text):
        input_ids = self.tokenizer_dpr(text, return_tensors='pt')["input_ids"]
        embeddings = self.model_dpr.forward(input_ids).pooler_output
        return embeddings

    # Function to calculate cosine similarity between query embedding and every corpus cell embedding
    def cos_sim(self, a, b):
        a_norm = torch.nn.functional.normalize(a, p=2, dim=1)
        b_norm = torch.nn.functional.normalize(b, p=2, dim=1)
        return torch.mm(a_norm, b_norm.transpose(0, 1))

    # Function that generates the context to be passed as RAG to the LLM (context = concatenation of relevant cell contents)
    def get_context(self, query):
        if self.rag_model == "dpr":
            index_high_score = self.dpr_search(query, self.rag_min_relevance, self.rag_max_results)
        elif self.rag_model == "bm25":
            index_high_score = self.bm25_search(query)
        if(len(index_high_score) > 0):
            rag_content = "\n".join(self.df["content"].iloc[index_high_score])
            return rag_content
        return "Aucun extrait du support de cours n'a été trouvé contenant des informations pertinentes sur la question posée par l'étudiant. Si vous ne connaissez pas non plus la réponse, informez l'étudiant que vous n'avez trouvé aucune information sur ce qui lui est demandé et recommandez-lui de contacter les professeurs responsables du cours."

    # Function that generates the reading recommendations (notebooks from the course Gitlab that are relevant and the student should review) as hyperlinks
    def get_recommendation(self, query_answer):
        if self.rag_model == "dpr":
            index_high_score = self.dpr_search(query_answer[:2500], self.recommendation_min_relevance, self.rag_max_results)
        elif self.rag_model == "bm25":
            index_high_score = self.bm25_search(query_answer)
        if(len(index_high_score) > 0):
            rag_courses =  self.df["file"].iloc[index_high_score].unique().tolist()
            rag_weeks =  self.df["folder"].iloc[index_high_score].unique().tolist()
            rag_recommendation = ", ".join([f"[`{rag_courses[i][:-3]}`](https://gitlab.dsi.universite-paris-saclay.fr/L1InfoInitiationScienceDonnees/Instructors/-/blob/main/{rag_weeks[i]}/{rag_courses[i]})" for i in range(len(rag_courses))])
            return rag_recommendation
        return None

    # Function that generates the context to be passed as RAG to the LLM (context = concatenation of relevant cell contents)
    def get_quiz_context(self, query):
        if(query == ""):
            notebook = random.choice(self.df.file.unique().tolist())
            self.quiz_subject = ""
            return "\n".join(self.df[self.df["file"] == notebook]["content"].dropna())
        elif(query in self.df.file.unique().tolist()):
            self.quiz_subject = ""
            return "\n".join(self.df[self.df["file"] == query]["content"].dropna())
        elif(query in [x.replace(".md", "") for x in self.df.file.unique().tolist()]):
            self.quiz_subject = ""
            return "\n".join(self.df[self.df["file"] == query+".md"]["content"].dropna())
        else:
            check_subject_relevance = self.dpr_search(query, 0.35, 5)
            if(len(check_subject_relevance) > 3):
                index_high_score = self.dpr_search(query, self.quiz_min_relevance, self.quiz_max_results)
                self.quiz_subject = f"de '{query}'"
                return "\n".join(self.df["content"].iloc[index_high_score])
            return None

    # IR function based on DPR to find relevant extracts
    def dpr_search(self, search_string, threshold, max_results):
        query_embedding = self.get_query_embedding(search_string)
        cos_scores = self.cos_sim(query_embedding, self.corpus_embeddings)[0]
        cos_scores_np = (-1) * np.sort(-cos_scores.detach().numpy())
        cos_idx_np = np.argsort(-cos_scores.detach().numpy())
        mask = cos_scores_np > threshold
        index_high_score = cos_idx_np[mask][:max_results]
        return index_high_score

    # IR function based on BM25 to find relevant extracts
    def bm25_search(self, search_string):
        search_tokens = word_tokenize(search_string)
        scores = self.bm25_index.get_scores(search_tokens)
        top_indexes = np.argsort(scores)[::-1][:self.rag_max_results]
        return top_indexes

    # LLM Generation function for aristote models
    def aristote_generate(self, messages, initial_response):
        generated_text = initial_response
        for chunk in self.model.stream(messages):
            generated_text += chunk.content
            display(Markdown(generated_text), clear=True)
        return generated_text

    # LLM Generation function for huggingface models
    def huggingface_generate(self, messages, initial_response):
        # Preprocess the question
        input_ids = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.device)
        
        generation_kwargs = {
            "input_ids": input_ids,
            "max_new_tokens": self.model_max_tokens,
            "eos_token_id": self.terminators,
            "pad_token_id": self.tokenizer.pad_token_id,
            "do_sample": True,
            "temperature": self.model_temperature,
            "top_p": 0.9,
            "streamer": self.streamer
        }
        # Generate answer and display it word by word as it is written (similar to ChatGPT user experience)
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()
        generated_text = initial_response
        for new_text in self.streamer:
            generated_text += new_text.replace("<|eot_id|>", "")
            display(Markdown(generated_text), clear = True)
        return generated_text

    def generate_quiz_questions_aristote(self):
        chunks = ""
        for chunk in self.model.stream(self.quiz_messages):
            chunks += chunk.content
            if "{" in chunks and "}" in chunks:
                init = chunks.find("{")
                end = chunks.find("}") + 1
                dict_string = chunks[init:end]
                true_dict = json.loads(dict_string)
                answers = [true_dict["bonne_réponse"]] + true_dict["mauvaises_réponses"]
                random.shuffle(answers)
                true_dict["toutes_réponses"] = answers
                self.questions_llm.append(true_dict)
                chunks = ""


    def generate_quiz_questions_huggingface(self):

        # Preprocess the question
        input_ids = self.tokenizer.apply_chat_template(
            self.quiz_messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.device)
        
        generation_kwargs = {
            "input_ids": input_ids,
            "max_new_tokens": 2048,
            "eos_token_id": self.terminators,
            "pad_token_id": self.tokenizer.pad_token_id,
            "do_sample": True,
            "temperature": self.model_temperature,
            "top_p": 0.9,
            "streamer": self.streamer
        }
        # Generate answer and display it word by word as it is written (similar to ChatGPT user experience)
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        generated_text = ""
        for new_text in self.streamer:
            generated_text += new_text.replace("<|eot_id|>", "")
            display(Markdown(generated_text), clear = True)
            if "{" in generated_text and "}" in generated_text:
                init = generated_text.find("{")
                end = generated_text.find("}") + 1
                dict_string = generated_text[init:end]
                true_dict = json.loads(dict_string)
                answers = [true_dict["bonne_réponse"]] + true_dict["mauvaises_réponses"]
                random.shuffle(answers)
                true_dict["toutes_réponses"] = answers
                self.questions_llm.append(true_dict)
                generated_text = ""
        return generated_text

        
        




    def display_question(self, index):
        if index >= self.num_questions:
            self.finish_quiz()
            return
            
        with self.out:
            clear_output(wait=True)
            if len(self.questions_llm) <= index:
                display(Markdown("### ⏳ Chargement de la question, veuillez patienter..."))
                while(len(self.questions_llm) <= index):
                    pass
            question = self.questions_llm[index]["énoncé"]
            right_answer = self.questions_llm[index]["bonne_réponse"]
            answers = self.questions_llm[index]["toutes_réponses"]
            clear_output(wait=True)
            display(Markdown(f"### Question {index+1}/{self.num_questions}: {question}"))
            
            radio_buttons = widgets.RadioButtons(
                options=answers,
                value=self.selected_answers[index],  # Selected value
                description="Choisissez l'option correcte:",
                disabled=False,
                layout={'width': 'max-content'},
            )
    
            display(radio_buttons)
    
            if index > 0:
                button_back = widgets.Button(description='Précédent', disabled=False)
            else:
                button_back = widgets.Button(description='Précédent', disabled=True)
            button_back.style.button_color = 'lightblue'
            if index < (self.num_questions - 1):
                button_next = widgets.Button(description='Suivant')
            else:
                button_next = widgets.Button(description='Finaliser')
            button_next.style.button_color = 'lightgreen'  
    
            button_box = widgets.HBox([button_back, button_next])
            display(button_box)
            
            def on_button_back_click(b):
                self.selected_answers[index] = radio_buttons.value
                self.display_question(index - 1)
    
            def on_button_next_click(b):
                self.selected_answers[index] = radio_buttons.value
                self.display_question(index + 1)
    
    
            button_back.on_click(on_button_back_click)
            button_next.on_click(on_button_next_click)
    
    # Function to finish and save results
    def finish_quiz(self):
        final_answers = self.questions_llm.copy()
        number_correct = 0
        with self.out:
            clear_output(wait=True)
            display(Markdown("# Quiz terminé !"))
            for i in range(len(final_answers)):
                final_answers[i]["réponse_sélectionnée"] = self.selected_answers[i]
                if final_answers[i]["réponse_sélectionnée"] == final_answers[i]["bonne_réponse"]:
                    number_correct += 1
                    display(Markdown(f"#### ✔️ Question {i+1}: {final_answers[i]["énoncé"]}"))
                    display(Markdown(f"**Réponse Sélectionnée :** {final_answers[i]["réponse_sélectionnée"]}"))
                    print("\n")
                else:
                    display(Markdown(f"#### ❌ Question {i+1}: {final_answers[i]["énoncé"]}"))
                    display(Markdown(f"**Réponse Sélectionnée :** {final_answers[i]["réponse_sélectionnée"]}"))
                    display(Markdown(f"**Réponse Correcte :** {final_answers[i]["bonne_réponse"]}"))
                    print("\n")
            display(Markdown(f"### 📜 Votre nombre de réponses correctes est de {number_correct}/{self.num_questions}."))
            print("\n")
            button_feedback = widgets.Button(description='Feedback')
            button_feedback.style.button_color = 'lightgreen' 
            display(button_feedback)
            def on_button_feedback_click(b):
                with self.out:
                    clear_output(wait=True)
                    prompt_feedback = f"Générez un feedback pour un étudiant à partir des réponses qu'il a données à un quiz de type QCM. Organisez votre feedback en rappelant toujours les questions et les réponses lorsque l'étudiant n'a plus accès au quiz, en expliquant pourquoi la bonne alternative est correcte et pourquoi les mauvaises alternatives sont incorrectes. Si l'élève a choisi l'alternative incorrecte, renforcez votre explication sur la source possible de la confusion qui l'a conduit à se tromper dans la question et soulignez, parmi les alternatives disponibles, celle qui est correcte. Récapitulatif du quiz : {final_answers}"
                    chunks = "### 📚 Feedback sur le quiz :\n"
                    for chunk in self.model.stream(prompt_feedback):
                        chunks += chunk.content
                        display(Markdown(chunks), clear=True)
            button_feedback.on_click(on_button_feedback_click)












    


    

    # Config the magic commands and display initial message
    def setup_magics(self):
        self.ip = get_ipython()
        if self.ip:
            self.ip.register_magic_function(self.ai_question, 'line_cell', 'ai_question')
            self.ip.register_magic_function(self.ai_code, 'line_cell', 'ai_code')
            self.ip.register_magic_function(self.ai_quiz, 'line', 'ai_quiz')
            self.ip.register_magic_function(self.ai_help, 'line', 'ai_help')
            display(Markdown("**UPSay AI Magic Commands** chargé avec succès ✅"))
            display(Markdown("Utilisez `%ai_help` pour accéder au Guide d'Utilisation."))

    # %ai_question magic command
    def ai_question(self, line="", cell=""):
        question = line + cell
        rag = self.get_context(question)
        rag_prompt = f" Voici un extrait du support de cours qui pourra vous être utile dans votre réponse à l'étudiant: {rag}"
        # Append the users's current question to the messages history
        self.messages_history.append({"role": "user", "content": question})
        # The messages history does not include the RAG results for every exchange. Only the RAG of the current question is present in the messages passed to the LLM
        if self.model_name == "aristote/mixtral":
            messages = [{"role": "user", "content": self.persona_prompt_qa + rag_prompt}, {"role": "assistant", "content": "Bien sûr, je serais ravi de vous aider avec vos questions sur la programmation et la science des données."}] + [x for x in self.messages_history]
        else:
            messages = [{"role": "system", "content": self.persona_prompt_qa + rag_prompt}] + [x for x in self.messages_history]
        initial_response = ""
        # Generate answer and display it word by word as it is written (similar to ChatGPT user experience)
        if self.model_name == "aristote/llama" or self.model_name == "aristote/mixtral":
            generated_text = self.aristote_generate(messages, initial_response)
        elif self.model_name == "huggingface/llama":
            generated_text = self.huggingface_generate(messages, initial_response)


        # Append the assistant's answer to the messages history
        self.messages_history.append({"role": "assistant", "content": generated_text})
        # Use the assistant's answer alongside the question to find possible recommendations for the student 
        recommendation = self.get_recommendation(question + " " + generated_text)
        if(recommendation):
            generated_text += "\n\n"
            recommendation_string = "💡 Pour plus d'informations sur ce sujet, il peut être utile de cliquer sur les liens pour réviser les cours :"
            # Also display the recommendation word by word to improve user experience (seamlessly integration with LLM answer)
            for word in recommendation_string.split():
                generated_text += word + ' '
                display(Markdown(generated_text), clear = True)
                time.sleep(0.03)
            display(Markdown(f"{generated_text}{recommendation}."), clear = True)
        # Limit history length to 10 exchanges user-assistant (i.e. max = 20 messages). If it passes this limit, delete first (oldest) exchange.
        if(len(self.messages_history)>20):
            self.messages_history.pop(0)
            self.messages_history.pop(0)

    # %ai_code magic command
    def ai_code(self, line="", cell=""):
        code_inst = line + cell
        # No RAG for now
        if self.model_name == "aristote/mixtral":
            messages = [{"role": "user", "content": self.persona_prompt_code}, {"role": "assistant", "content": "Bien sûr, je serais ravi de vous aider avec vos codes python."},  {"role": "user", "content": code_inst}]
        else:
            messages = [{"role": "system", "content": self.persona_prompt_code}, {"role": "user", "content": code_inst}]
        initial_response = "⏳ Une fois la réponse complétée, le code sera déplacé dans une nouvelle cellule juste en dessous.\n\n"
        
        if self.model_name == "aristote/llama" or self.model_name == "aristote/mixtral":
            generated_text = self.aristote_generate(messages, initial_response)
        elif self.model_name == "huggingface/llama":
            generated_text = self.huggingface_generate(messages, initial_response)

        generated_text = generated_text.replace(initial_response, "")
        # Chech for the code block inside of the generated answer
        if '```python' in generated_text and '```\n' in generated_text:
            code_init = generated_text.find('```python') + len('```python')
            code_end = generated_text.find('```\n')
            # Put a comment before
            if(cell == ""):
                code = "# ⚠️ Attention : Ce code a été généré par une Intelligence Artificielle et est donc sujet à des erreurs\n" + f"# Code généré à partir de l'instruction suivante : '{code_inst}'\n" + generated_text[code_init:code_end]
            else:
                code = "# ⚠️ Attention : Ce code a été généré par une Intelligence Artificielle et est donc sujet à des erreurs\n" + f"'''\nCode généré à partir de l'instruction suivante : \n{code_inst}'''\n" + generated_text[code_init:code_end]
            code_remove = generated_text[(code_init - len('```python')):(code_end + len('```\n'))]
            generated_text = generated_text.replace(code_remove, "")
            generated_text += "\n\n" + "Le code généré par l'IA a été inséré dans la cellule ci-dessous ⬇️"
            self.ip.set_next_input(code) # Generate new cell with code
        display(Markdown(generated_text), clear = True)



    # %ai_question magic command
    def ai_quiz(self, line=""):
        self.selected_answers = [None, None, None, None, None]
        cours_content = self.get_quiz_context(line)
        if(cours_content == None):
            display(Markdown("#### Not related to the class"))
        else:
            content_prompt = f"Cours à utiliser pour générer le questionnaire : {cours_content}"
            # The messages history does not include the RAG results for every exchange. Only the RAG of the current question is present in the messages passed to the LLM
            if self.model_name == "aristote/mixtral":
                self.quiz_messages = [{"role": "user", "content": self.persona_prompt_quiz}, {"role": "assistant", "content": "Bien sûr, je générerai le questionnaire sur le cours qui me sera donné et je le renverrai dans le format indiqué."}, {"role": "user", "content": content_prompt}]
            else:
                self.quiz_messages = [{"role": "system", "content": self.persona_prompt_quiz}, {"role": "user", "content": content_prompt}]
            
            self.questions_llm = []
            self.num_questions = 5
            # Generate answer and display it word by word as it is written (similar to ChatGPT user experience)
            if self.model_name == "aristote/llama" or self.model_name == "aristote/mixtral":
                Thread(target=self.generate_quiz_questions_aristote).start()
                
            elif self.model_name == "huggingface/llama":
                raise ValueError("The %ai_quiz command is currently only available for aristote models.")
                
                
            self.out = widgets.Output()
            display(self.out)
            # Start the interactive loop
            self.display_question(0)


    
    # %ai_help magic command
    def ai_help(self, line):
        display(Markdown("### Guide d'Utilisation"))
        display(Markdown("L'**UPSay AI Magic Commands** est un ensemble d'outils expérimentaux d'IA Générative inspiré de jupyter-ai et actuellement en cours de développement à l'Université Paris-Saclay."))
        display(Markdown("Liste des Commandes Magiques :"))
        display(Markdown("---"))
        display(Markdown("#### **`%ai_question`**"))
        display(Markdown("**Description :** Commande magique conçue pour les questions/réponses (Q&R)."))
        display(Markdown("**Mode d'emploi :** Placez la commande dans la première ligne d'une cellule vide, suivie d'une question sur la même ligne. La réponse apparaîtra au format Markdown juste en dessous de la cellule."))
        display(Markdown("**Exemple d'utilisation :**"))
        display(Markdown(f"<span style='color: grey;'>[ 42 ] : </span>`%ai_question Quelle est la différence entre causalité et corrélation ?{''.join(["\t" for i in range(50)])}`"))
        display(Markdown("**Note :** Vous pouvez utiliser **`%%ai_question`** avec un double % si vous préférez utiliser plusieurs lignes pour formuler votre question."))
        display(Markdown("---"))
        display(Markdown("#### **`%ai_code`**"))
        display(Markdown("**Description :** Commande magique conçue pour la génération de code (python)."))
        display(Markdown("**Mode d'emploi :** Placez la commande dans la première ligne d'une cellule vide, suivie des instructions pour la génération du code sur la même ligne. Le code généré apparaîtra dans une nouvelle cellule."))
        display(Markdown("**Exemple d'utilisation :**"))
        display(Markdown(f"<span style='color: grey;'>[ 42 ] : </span>`%ai_code Fonction qui calcule le déterminant d'une matrice numpy.{''.join(["\t" for i in range(50)])}`"))
        display(Markdown("**Note :** Vous pouvez utiliser **`%%ai_code`** avec un double % si vous préférez utiliser plusieurs lignes pour formuler vos intructions de code."))
        display(Markdown("---"))
        display(Markdown("#### **`%ai_quiz`**"))
        display(Markdown("**Description :** Commande magique conçue pour la génération de quiz style QCM."))
        display(Markdown("**Mode d'emploi :** Il existe trois manières d'utiliser cette commande, en fonction du sujet du quiz que vous souhaitez obtenir :"))
        display(Markdown("• Placez la commande toute seule dans la première ligne d'une cellule vide : pour générer un quiz sur une leçon (notebook du cours) aléatoire."))
        display(Markdown("• Placez la commande dans la première ligne d'une cellule vide, suivie du sujet souhaité pour le quiz sur la même ligne : pour générer un quiz sur un sujet spécifique."))
        display(Markdown("• Placez la commande dans la première ligne d'une cellule vide, suivie du nom d'une leçon (notebook du cours) au format CMx ou CMx.md sur la même ligne : pour générer un quiz sur une leçon spécifique."))
        display(Markdown("**Exemples d'utilisation :**"))
        display(Markdown(f"<span style='color: grey;'>[ 42 ] : </span>`%ai_quiz{''.join(["\t" for i in range(50)])}`"))
        display(Markdown(f"<span style='color: grey;'>[ 42 ] : </span>`%ai_quiz réseau de neurones{''.join(["\t" for i in range(50)])}`"))
        display(Markdown(f"<span style='color: grey;'>[ 42 ] : </span>`%ai_quiz CM4{''.join(["\t" for i in range(50)])}`"))
        display(Markdown("---"))
        
