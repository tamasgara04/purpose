from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

class CustML:
    tokenizer = None
    model = None
    context = None

    def __init__(self) -> None:
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
        self.model = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
        self.context = """
        Germany, officially the Federal Republic of Germany, is a country in Central Europe. It is bordered to the north by the North Sea, Denmark, and the Baltic Sea; to the east by Poland and the Czech Republic; to the south by Austria and Switzerland; and to the west by France, Luxembourg, Belgium, and the Netherlands. Germany is the second-most populous country in Europe after Russia, and the most populous member state of the European Union.
        Germany has a rich cultural history, with significant contributions to art, music, literature, philosophy, science, and technology. It has a highly developed economy and is known for its engineering prowess, automotive industry, and world-class infrastructure. Berlin is the capital and largest city of Germany, known for its vibrant culture, historical landmarks, and diverse population.
        Germany has played a central role in European history, from the Holy Roman Empire to the Protestant Reformation and the two World Wars of the 20th century. It is a federal parliamentary republic, with a democratic government and a strong emphasis on social welfare and environmental sustainability. The country is also a global leader in renewable energy and environmental conservation.
        """

    def get_extra_content(self, new_context):
        formatted_context = "Users from database: \n"
        for line in new_context:
            formatted_context += f'Name: {line["name"]}, Email: {line["email"]}\n'
        return formatted_context

    # Define a function to process text and obtain sentiment prediction
    def answer_question(self, question, extra_context=""):
        # Get extra content
        extra_context = self.get_extra_content(extra_context)

        # Tokenize inputs
        inputs = self.tokenizer(question, self.context + extra_context, return_tensors="pt")

        # Perform inference
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Get the predicted answer span
        answer_start_scores = outputs.start_logits
        answer_end_scores = outputs.end_logits

        # Find the tokens with the highest probability of being the start and end of the answer
        answer_start = torch.argmax(answer_start_scores)
        answer_end = torch.argmax(answer_end_scores) + 1

        # Decode the tokens to get the answer
        answer = self.tokenizer.decode(inputs["input_ids"][0][answer_start:answer_end])

        return answer
    