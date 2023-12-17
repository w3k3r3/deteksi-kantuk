import cv2
import os
import torch
from PIL import Image
from io import BytesIO


one = [ "", "one ", "two ", "three ", "four ",
        "five ", "six ", "seven ", "eight ",
        "nine ", "ten ", "eleven ", "twelve ",
        "thirteen ", "fourteen ", "fifteen ",
        "sixteen ", "seventeen ", "eighteen ",
        "nineteen "];

ten = [ "", "", "twenty ", "thirty ", "forty ",
        "fifty ", "sixty ", "seventy ", "eighty ",
        "ninety "];

class project_pcd:

    def __init__(self, model_name):
        self.model = self.load_model(model_name)
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)

    def load_model(self, model_name):
        model = torch.hub.load('./yolov5', 'custom', path=model_name, source='local')  # local repo
        return model

    def class_to_label(self, x):
        return self.classes[int(x)]

    def numToWords(self,n, s):
        str = ""
        
        if (n > 19):
            str += ten[n // 10] + one[n % 10]
        else:
            str += one[n]
    
        if(n != 0):
            str += s
    
        return str

    def convertToWords(self,n):
        out = ""
        out += self.numToWords((n // 10000000),"crore ")
        out += self.numToWords(((n // 100000) % 100),"lakh ")
        out += self.numToWords(((n // 1000) % 100),"thousand ")
        out += self.numToWords(((n // 100) % 10),"hundred ")
        
        if (n > 100 and n % 100):
            out += "and "
        out += self.numToWords((n % 100), "")
        
        return out

    def get_text(self,labelCnt):
        text = "he is"
        
        noOfLabels,counter = len(labelCnt),0
        for k,v in labelCnt.items():
            if(k== "tidak kantuk"):
                k = "not sleepy"
            if(k== "kantuk"):
                k = "sleepy"
            text += " {} {} ".format(k,"bro")
            if(counter != noOfLabels-1):
                text += 'and'
            counter += 1

        return text


    def get_detected_image(self,img):
        imgs = [img]
        
        results = self.model(imgs, size=416)
        
        results.print()
        
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        n = len(labels)
        labelCnt = {}
        for i in range(n):
            classLabel = self.classes[int(labels[i])]
            row = cord[i]
            
            print("{} is detected with {} probability.".format(classLabel, row[4]))
            if classLabel in labelCnt:
                labelCnt[classLabel] += 1
            else:
                labelCnt[classLabel] = 1

        text = self.get_text(labelCnt)
        print("{} This is from yolo_detection.py".format(text))
        
        print('\n', results.xyxy[0])
        results.ims
        results.render()
        
        return results.ims[0],text





def run_model(img):
    obj = project_pcd(
        model_name='./yolov5/runs/train/exp/weights/best.pt'
    )
    detected_labels_text = ""
    detected_img,detected_labels_text = obj.get_detected_image(img)
    return detected_img, detected_labels_text