import json
import os


class SaveManager:


    def __init__(self,file_path="data/scores.json"):
        self.file_path=file_path

    #load scores from json file
    def load_scores(self):

        if not os.path.exists(self.file_path):
            return {}

        with open(self.file_path,"r") as file:
            return json.load(file)

    #save scores to json file
    def save_scores(self,scores):

        os.makedirs(
            os.path.dirname(self.file_path),
            exist_ok=True
        )

        with open(self.file_path,"w") as file:
            json.dump(scores,file,indent=4)