# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from tadano_summarizer import Tadano_Summarizer
from huliu_summarizer import HuLiu_Summarizer
from gerani_summarizer import Gerani_Summarizer
from ganesan_summarizer import Ganesan_Summarizer
from opizere_summarizer import Opizere_Summarizer
from opizera_summarizer import Opizera_Summarizer
from buscape_reader import BuscapeCorpusReader
from reli_reader import ReLiCorpusReader
import sys
import os
import codecs
if __name__ == '__main__':
    try:
        summarizer = sys.argv[1]
        index_item = int(sys.argv[2])
        num_aspects = int(sys.argv[3])
    except:
        print '<font color="red">The parameters are incorrect</font>'# for web version
	raise ValueError("The parameters are incorrect")

    items = ["Galaxy-SIII", "Samsung-Smart-TV", "LG-Smart-TV", "Iphone-5", "Capitaes-da-Areia", "Crepusculo", "Ensaio-Sobre-a-Cegueira", 
    "Fala-Serio-Amiga", "Fala-Serio-Amor", "Fala-Serio-Mae", "Fala-Serio-Pai", "Fala-Serio-Professor", "O-Apanhador-no-Campo-de-Centeio",
    "O-Outro-Lado-da-Meia-Noite", "O-Reverso-da-Medalha", "Se-Houver-Amanha", "1984"]
    summary = ""
        
    if index_item < 4:
        aspect_manager = BuscapeCorpusReader("../resource/corpus_buscape")
        item_path = os.path.join("../resource/reviews_buscape/", items[index_item])
    else:
        aspect_manager = ReLiCorpusReader("../resource/corpus_reli_mini")
        item_path = os.path.join("../resource/reviews_reli/", items[index_item])
    
    if summarizer == "huliu":
        huliu = HuLiu_Summarizer(items[index_item], item_path, aspect_manager)
        summary = huliu.create_summary(None, num_aspects, 1, False)
    elif summarizer == "tadano":
        tadano = Tadano_Summarizer(items[index_item], item_path, aspect_manager)
        summary = tadano.create_summary(None, num_aspects, 1, False)
    elif summarizer == "opizere":
        opizere = Opizere_Summarizer(items[index_item], item_path, aspect_manager)
        summary = opizere.create_summary(None, num_aspects, 1, False)
    elif summarizer == "ganesan":
        ganesan = Ganesan_Summarizer(items[index_item], item_path, aspect_manager)
        summary = ganesan.create_summary(None, num_aspects, False)
    elif summarizer == "gerani":
        gerani = Gerani_Summarizer(items[index_item], item_path, aspect_manager)
        summary = gerani.create_summary(None, num_aspects, False)
    elif summarizer == "opizera":
        opizera = Opizera_Summarizer(items[index_item], item_path, aspect_manager)
        summary = opizera.create_summary(None, num_aspects, False)
    
    summary = summary.replace('"', '')
    summary = summary.replace("\n", "<br>")
    print summary.encode('utf-8')
