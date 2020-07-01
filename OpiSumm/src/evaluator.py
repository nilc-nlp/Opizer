# -*- coding: utf-8 -*-
'''
Created on 08/05/2015

@author: Roque Lopez
'''
from __future__ import unicode_literals
from tadano_summarizer import Tadano_Summarizer
from huliu_summarizer import HuLiu_Summarizer
from gerani_summarizer import Gerani_Summarizer
from ganesan_summarizer import Ganesan_Summarizer
from opizere_summarizer import Opizere_Summarizer
from opizera_summarizer import Opizera_Summarizer
from buscape_reader import BuscapeCorpusReader
from reli_reader import ReLiCorpusReader
from nltk.tokenize import RegexpTokenizer
from utils import make_dir, read_file, join_files, Capturing
from prettytable import PrettyTable
import os
import re
import shutil
import codecs
import csv

tokenizer = RegexpTokenizer(r'\w+')

class Evaluator(object):
    '''
    Class to evaluate the performance of different summarizers (ROUGE and DUC forms)
    '''

    def __init__(self, words):
        self.__words = words
        self.__buscape_reader = BuscapeCorpusReader("../resource/corpus_buscape")
        self.__reli_reader = ReLiCorpusReader("../resource/corpus_reli_mini")

    def create_models(self, input_path, output_path, flag_summary): 
        ''' Create the gold standard corpus (manual summaries) '''
        if flag_summary == "E": 
            type_summary = "Extrativos"
        elif flag_summary == "A":
            type_summary = "Abstrativos"
        else:
            raise ValueError("Invalid option")

        models_name = ["A", "B", "C", "D", "E"]
        folders = sorted(os.listdir(input_path))

        for folder in folders:
            file_list = os.listdir(os.path.join(input_path, folder, type_summary))
            make_dir(os.path.join(output_path, folder, "models"))
            
            for i in range(len(models_name)):
                shutil.copy(os.path.join(input_path, folder, type_summary, file_list[i]), os.path.join(output_path, folder, "models", "1_model%s.txt" % models_name[i]))
                if flag_summary == "E":
                    self.__replace_id(os.path.join(output_path, folder, "models", "1_model%s.txt" % models_name[i]))

    def generate_summaries(self, general_output_path):
        ''' Generate summaries for book and product opinions '''
        products = os.listdir("../resource/reviews_buscape/")
        books = os.listdir("../resource/reviews_reli/")

        for book in books:
            print book
            output_path = os.path.join(general_output_path, book, "summaries")
            make_dir(output_path)
            #self.generate_rsumm(book, output_path)
            self.generate_tadano(book, os.path.join("../resource/reviews_reli/", book), output_path, self.__reli_reader)
            #self.generate_huliu(book, os.path.join("../resource/reviews_reli/", book), output_path, self.__reli_reader)
            #self.generate_gerani(book, os.path.join("../resource/reviews_reli/", book), output_path, self.__reli_reader)
            #self.generate_ganesan(book, output_path)
            

        for product in products:
            print product
            output_path = os.path.join(general_output_path, product, "summaries")
            make_dir(output_path)
            #self.generate_rsumm(product, output_path)
            self.generate_tadano(product, os.path.join("../resource/reviews_buscape/", product), output_path, self.__buscape_reader)
            #self.generate_huliu(product, os.path.join("../resource/reviews_buscape/", product), output_path, self.__buscape_reader)
            #self.generate_gerani(product, os.path.join("../resource/reviews_buscape/", product), output_path, self.__buscape_reader)
            #self.generate_ganesan(product, output_path)

    def generate_rsumm(self, folder, output_path):
        ''' Generate a summary using RSumm summarizer for a desirable size '''
        os.chdir("/home/roque/Downloads/RSumm/bin")
        rate = 0.92
        diff_old = self.__words
        summary = ""

        while True:
            os.system("./Summ -profundo ../opinions/%s.txt %.2f > /dev/null" % (folder, rate))
            text = read_file("/home/roque/Downloads/RSumm/bin/summary.prof")         
            words =  len(tokenizer.tokenize(text))
            diff_current = abs(self.__words - words)

            if diff_current <= diff_old:
                diff_old = diff_current
                summary = text
                rate -= 0.02
            else:
                break

        with codecs.open(os.path.join(output_path, "1_summary.txt"), 'w','utf-8') as fout:
            fout.write(summary)

    def generate_tadano(self, folder, folder_path, output_path, aspect_manager):
        ''' Generate a summary using Tadano summarizer for a desirable size '''
        aspects =  2
        comments =  1
        diff_old = self.__words
        summary = None

        while True:
            tadano = Tadano_Summarizer(folder, folder_path, aspect_manager)
            text = tadano.create_summary("", aspects, comments, False)     
            words =  len(tokenizer.tokenize(text))
            diff_current = abs(self.__words - words)

            if diff_current < diff_old:
                summary = text
                diff_old = diff_current
                aspects += 1
                if comments > 1: comments +=1
            elif comments == 1:
                comments += 1
            else:
                break
                
        with codecs.open(os.path.join(output_path, "1_summary.txt"), 'w','utf-8') as fout:
            fout.write(summary)

    def generate_huliu(self, folder, folder_path, output_path, aspect_manager):
        ''' Generate a summary using HuLiu summarizer for a desirable size '''
        aspects =  2
        comments =  1
        diff_old = self.__words
        summary = None

        while True:
            hu_liu = Opizere_Summarizer(folder, folder_path, aspect_manager)
            text = hu_liu.create_summary("", aspects, comments, False) 
            clean_text = self.__clean_text_huliu(text)      
            words =  len(tokenizer.tokenize(clean_text))
            diff_current = abs(self.__words - words)

            if diff_current < diff_old:
                summary = clean_text
                summary2 = text
                diff_old = diff_current
                aspects += 1
                if comments > 1: comments +=1
            elif comments == 1:
                comments += 1
            else:
                break

        with codecs.open(os.path.join(output_path, "1_summary.txt"), 'w','utf-8') as fout:
            fout.write(summary)   
                
    def generate_gerani(self, folder, folder_path, output_path, aspect_manager):
        ''' Generate a summary using Gerani summarizer for a desirable size '''
        aspects =  5
        diff_old = self.__words
        summary = None

        while True:
            gerani = Opizera_Summarizer(folder, folder_path, aspect_manager)
            text = gerani.create_summary("", aspects, False)        
            words =  len(tokenizer.tokenize(text))
            diff_current = abs(self.__words - words)

            if diff_current < diff_old:
                summary = text
                diff_old = diff_current
                aspects += 1
            else:
                break

        with codecs.open(os.path.join(output_path, "1_summary.txt"), 'w','utf-8') as fout:
            fout.write(summary)

    def generate_ganesan(self, folder, output_path):
        ''' Generate a summary using Ganesan summarizer for a desirable size '''
        diff_old = self.__words
        summary = ""
        text = ""
        ganesan_file = "../resource/automatic_summaries/ganesan/%s.sum" % folder

        with codecs.open(ganesan_file, 'r', 'utf-8') as fin:
            sentences = fin.readlines()

        for sentence in sentences:
            text += sentence        
            words =  len(tokenizer.tokenize(text))
            diff_current = abs(self.__words - words)

            if diff_current < diff_old:
                summary = text
                diff_old = diff_current
            else:
                break

        with codecs.open(os.path.join(output_path, "1_summary.txt"), 'w','utf-8') as fout:
            fout.write(summary)

    def calculate_rouge(self, folder_path):
        ''' Calculate ROUGE measure for a set of summaries  using the ROUGE toolkit '''
        current_dir =  os.getcwd()
        os.chdir("/home/roque/summeval/")
        with Capturing() as output:
        	os.system("./execute_rouge.sh")
        os.chdir(current_dir)
        f = 0.0
        p = 0.0
        r = 0.0

        file_list =  sorted(os.listdir(folder_path))
        list_size =  len(file_list)

        for rouge_file in file_list:
            with codecs.open(os.path.join(folder_path, rouge_file), 'r','utf-8') as handle:
                lines = handle.readlines()
            r_value = float(re.match('1 ROUGE-2 Average_R: (0\.\d+) \(', lines[16]).group(1))
            p_value = float(re.match('1 ROUGE-2 Average_P: (0\.\d+) \(', lines[17]).group(1))
            f_value = float(re.match('1 ROUGE-2 Average_F: (0\.\d+) \(', lines[18]).group(1))
            r += r_value
            p += p_value
            f += f_value
            print rouge_file, "%.3f %.3f %.3f" % (r_value, p_value, f_value)
        print "Average %.3f %.3f %.3f" % (r / list_size, p / list_size, f / list_size)

    def calculate_rouge1(self, folder_path):
        ''' Calculate ROUGE measure for a set of summaries  using the ROUGE toolkit '''
        current_dir =  os.getcwd()
        os.chdir("/home/roque/summeval/")
        with Capturing() as output:
        	os.system("./execute_rouge.sh")
        os.chdir(current_dir)
        
        file_list =  ["Galaxy-SIII", "Iphone-5", "LG-Smart-TV", "Samsung-Smart-TV"]
        list_size =  len(file_list)
        f = 0.0
        p = 0.0
        r = 0.0

        for rouge_file in file_list:
            with codecs.open(os.path.join(folder_path, rouge_file), 'r','utf-8') as handle:
                lines = handle.readlines()
            r_value = float(re.match('1 ROUGE-2 Average_R: (0\.\d+) \(', lines[16]).group(1))
            p_value = float(re.match('1 ROUGE-2 Average_P: (0\.\d+) \(', lines[17]).group(1))
            f_value = float(re.match('1 ROUGE-2 Average_F: (0\.\d+) \(', lines[18]).group(1))
            r += r_value
            p += p_value
            f += f_value
        print "2 Average & %.3f & %.3f & %.3f" % (r / list_size, p / list_size, f / list_size)
        
        f = 0.0
        p = 0.0
        r = 0.0

        for rouge_file in file_list:
            with codecs.open(os.path.join(folder_path, rouge_file), 'r','utf-8') as handle:
                lines = handle.readlines()
            r_value = float(re.match('1 ROUGE-L Average_R: (0\.\d+) \(', lines[28]).group(1))
            p_value = float(re.match('1 ROUGE-L Average_P: (0\.\d+) \(', lines[29]).group(1))
            f_value = float(re.match('1 ROUGE-L Average_F: (0\.\d+) \(', lines[30]).group(1))
            r += r_value
            p += p_value
            f += f_value
        print "L Average & %.3f & %.3f & %.3f" % (r / list_size, p / list_size, f / list_size)

        file_list = ["1984", "Capitaes-da-Areia", "Crepusculo", "Ensaio-Sobre-a-Cegueira", "Fala-Serio-Amiga", "Fala-Serio-Amor", "Fala-Serio-Mae", 
            "Fala-Serio-Pai", "Fala-Serio-Professor", "O-Apanhador-no-Campo-de-Centeio", "O-Outro-Lado-da-Meia-Noite", "O-Reverso-da-Medalha", "Se-Houver-Amanha"]
        list_size =  len(file_list)
        f = 0.0
        p = 0.0
        r = 0.0

        for rouge_file in file_list:
            with codecs.open(os.path.join(folder_path, rouge_file), 'r','utf-8') as handle:
                lines = handle.readlines()
            r_value = float(re.match('1 ROUGE-2 Average_R: (0\.\d+) \(', lines[16]).group(1))
            p_value = float(re.match('1 ROUGE-2 Average_P: (0\.\d+) \(', lines[17]).group(1))
            f_value = float(re.match('1 ROUGE-2 Average_F: (0\.\d+) \(', lines[18]).group(1))
            r += r_value
            p += p_value
            f += f_value
        print "2 Average & %.3f & %.3f & %.3f" % (r / list_size, p / list_size, f / list_size)

        f = 0.0
        p = 0.0
        r = 0.0

        for rouge_file in file_list:
            with codecs.open(os.path.join(folder_path, rouge_file), 'r','utf-8') as handle:
                lines = handle.readlines()
            r_value = float(re.match('1 ROUGE-L Average_R: (0\.\d+) \(', lines[28]).group(1))
            p_value = float(re.match('1 ROUGE-L Average_P: (0\.\d+) \(', lines[29]).group(1))
            f_value = float(re.match('1 ROUGE-L Average_F: (0\.\d+) \(', lines[30]).group(1))
            r += r_value
            p += p_value
            f += f_value
        print "L Average & %.3f & %.3f & %.3f" % (r / list_size, p / list_size, f / list_size)

        f = 0.0
        p = 0.0
        r = 0.0

        file_list =  sorted(os.listdir(folder_path))
        list_size =  len(file_list)

        for rouge_file in file_list:
            with codecs.open(os.path.join(folder_path, rouge_file), 'r','utf-8') as handle:
                lines = handle.readlines()
            r_value = float(re.match('1 ROUGE-2 Average_R: (0\.\d+) \(', lines[16]).group(1))
            p_value = float(re.match('1 ROUGE-2 Average_P: (0\.\d+) \(', lines[17]).group(1))
            f_value = float(re.match('1 ROUGE-2 Average_F: (0\.\d+) \(', lines[18]).group(1))
            r += r_value
            p += p_value
            f += f_value
        print "2 Average & %.3f & %.3f & %.3f" % (r / list_size, p / list_size, f / list_size)

        f = 0.0
        p = 0.0
        r = 0.0

        for rouge_file in file_list:
            with codecs.open(os.path.join(folder_path, rouge_file), 'r','utf-8') as handle:
                lines = handle.readlines()
            r_value = float(re.match('1 ROUGE-L Average_R: (0\.\d+) \(', lines[28]).group(1))
            p_value = float(re.match('1 ROUGE-L Average_P: (0\.\d+) \(', lines[29]).group(1))
            f_value = float(re.match('1 ROUGE-L Average_F: (0\.\d+) \(', lines[30]).group(1))
            r += r_value
            p += p_value
            f += f_value
        print "L Average & %.3f & %.3f & %.3f" % (r / list_size, p / list_size, f / list_size)

    def calculate_duc(self, file_path):
        ''' Calculate the results of DUC forms '''
        position_summarizers = [2,3,0,2,1,3]# [0,2,3,1,0,1]A [1,0,1,3,2,0]E [2,3,0,2,1,3]R [3,1,2,0,3,2]H
        duc_values = {}

        with open(file_path, 'rb') as csvfile:
            rows = list(csv.reader(csvfile, delimiter=str(u','), quoting=csv.QUOTE_NONE))
            num_rows = float(len(rows))

            for row in rows:
                unicode_row = [x.decode('utf8').strip() for x in row]
                for index, position in enumerate(position_summarizers):
                    if index not in duc_values: duc_values[index] = [0, 0, 0, 0, 0, 0]
                    position = index * 4 + position
                    new_values = self.__get_duc_values(position, unicode_row)
                    duc_values[index] = [x + y for x, y in zip(duc_values[index], new_values)]

        total_values = [0, 0, 0, 0, 0, 0]
        items = ["Samsung Smart TV", "Iphone 5", "Samsung Galaxy S III", "Crepúsculo", "Ensaio sobre a Cegueira", "Fala sério, professor!"]
        num_items = float(len(items))
        table = PrettyTable(["Item", "G", "NR", "CR", "F", "EC","U"])
        table.align["Item"] = "l" 

        for id_item, duc_values in duc_values.items():
            values_by_item = [round(x / num_rows, 3) for x in duc_values]
            total_values = [x + y for x, y in zip(total_values, values_by_item)]
            table.add_row([items[id_item]] + values_by_item)

        table.add_row(["Average"] + [round(x / num_items, 3) for x in total_values])
        print table


    def __get_duc_values(self, position, row):
        ''' Calculate the results of DUC forms for a specific summarizer '''
    	duc_values = []
        for i in range(6):
            duc_values.append(int(row[position * 6 + i + 2][0]))

        return duc_values

    def __clean_text_huliu(self, text):
        ''' Return the HuLiu summaries without the information about aspects or sentences '''
        tmp_text = ""
        for line in text.split("\n"):
            line = line.strip()
            if not line.startswith("Aspecto:") and not line.startswith("Sentenças Positivas:") and not line.startswith("Sentenças Negativas:"):
                tmp_text += line[2:] + "\n"

        return tmp_text.strip()

    def __replace_id(self, file_path):
        ''' Remove the ID sentences in extractive summaries '''
        with codecs.open(file_path, 'r', 'utf-8') as f:
            text = f.read()
        new_text = re.sub(r'<D.+_S.+>', '', text)
        with codecs.open(file_path, 'w', 'utf-8') as f:
            f.write(new_text.strip())

if __name__ == '__main__':
    print "Starting..."
    input_path = "/home/roque/Dropbox/Code/SummariesAnnotation/resource/manual_summaries/"
    output_path = "../resource/rouge/"
    #join_files("../resource/reviews_buscape/","/home/roque/summeval/rsumm/opinions/")
    #join_files("../resource/reviews_reli/","/home/roque/summeval/rsumm/opinions/")

    e = Evaluator(100)
    #e.create_models(input_path, output_path, "E")
    e.generate_summaries(output_path)
    #e.calculate_rouge("/home/roque/Downloads/Rouge/ROUGE/data/")
    #e.calculate_duc("../resource/duc_form.csv")
    print "Finished"
