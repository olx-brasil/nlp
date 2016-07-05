# -*- coding: utf-8 -*-

import re
import pickle
from nlp.resource import Resource

class TagCleaner:
    model = None
    split_regex = re.compile('\W+', re.U)

    def __init__(self):
        pass

    def loadModel(self, modelName):
        resource_package = __name__
        with open(Resource.getResourcePath('data', "%s.dat" % modelName), 'r') as f:
            self.model = pickle.load(f)

    def getModel(self):
        return self.model

    def cleanNoWords(self, text):
        return re.sub(r'\w*\d+\w*', '', text)

    def tokenize(self, text):
      return [t for t in re.split(self.split_regex, text.lower()) if len(t) > 1 or t in ['a','e','o']]

    def tag(self, words):
      return self.model.tag(words)

    def getWindowList(self, x):
      aux = [0] * len(x)
      for idx in range(0,len(x)-4):
        if (x[idx][1]==None or x[idx][1]=='N' or x[idx][1]=='N|EST') and \
           (x[idx+1][1]==None or x[idx+1][1]=='N'  or x[idx+1][1]=='N|EST') and \
           (x[idx+2][1]==None or x[idx+2][1]=='N'  or x[idx+2][1]=='N|EST') and \
           (x[idx+3][1]==None or x[idx+3][1]=='N'  or x[idx+3][1]=='N|EST') and \
           (x[idx+4][1]==None or x[idx+4][1]=='N'  or x[idx+4][1]=='N|EST'):
          aux[idx]   = 1
          aux[idx+1] = 1
          aux[idx+2] = 1
          aux[idx+3] = 1
          aux[idx+4] = 1
      for idx, val in enumerate(x):
          x[idx] += (str(aux[idx]), )
      return x

    def filterBodyDel(self, text):
      return [t for t in text if t[2]=='0']

    def filterBodyMorf(self, text):
      return [t[0] for t in text if t[1] in [None, 'N', 'V', 'PCP', 'ADJ']]

    def countKeep(self, text):
      count = 0
      for i in text:
        if i[2] == '0':
          count+=1
      return count

    def countDel(self, text):
      count = 0
      for i in text:
        if i[2] == '1':
          count+=1
      return count

    def countN(self, text):
      count = 0
      for i in text:
        if i[1] == 'N':
          count+=1
      return count

    def processWords(self, words):
        return self.getWindowList(self.tag(words))

    def filterTokens(self, tokens):
        return self.filterBodyMorf(self.filterBodyDel(tokens))

    def cleanBody(self, body):
        body_clean = self.cleanNoWords(body)
        body_token = self.tokenize(body_clean)

        body_tagg = self.processWords(body_token)
        body_filt = self.filterTokens(body_tagg)

        return " ".join(body_filt)

def run():
    tag_cleaner = TagCleaner()
    tag_cleaner.loadModel('tagger')

    body_raw = u'IMAGENS MERAMENTE ILUSTRATIVAS, NÃO TEMOS O VEÍCULO DA FOTO. -<br><br>TRABALHAMOS SEU PERFIL PARA APROVAÇÃO DO SEU FINANCIAMENTO.<br><br>APROVAMOS E ENTREGAMOS QUALQUER VEÍCULO COM OU SEM ENTRADA !!<br><br>FACILITO FINANCIAMENTO PARA:<br>°AUTONOMOS<br>°BAIXA RENDA<br>°PESSOAS SEM EXPERIÊNCIA DE CRÉDITO<br>°DIFICULDADES DE APROVAÇÃO<br>°RECUSAS EM BANCOS<br>°ENTRE OUTRAS <br><br>- AQUI SIM VOCÊ CONSEGUE SEU FINANCIAMENTO DE QUALQUER VEÍCULO NO MERCADO. -<br><br>EXECUTIVO DE VENDAS : WELTON <br>WHATSAPP : (61) 98663-4133 <br>FIXO : (61) 3024-9332 <br><br>Filtro de busca:<br>Omega, Bravo, Ford ka, Honda Civic, Fit, Peugeot 207, uno, City, Kia Cerato, Chery QQ, Citroen C3 Cooper, 307, Bmw X1, Fiesta, Focus, Hyundai i30, Jeep, Audi A3, x6, Face, Aircross, Punto, Ford Fusion, ix35, sonata, Picanto, 3008, Renault Sandero, Ssangyong, A1, R8, Chevrolet Camaro, Citroen C4, 500, Edge, Mitsubishi Asx, 408, Fluence, Malibu, Dodge Journey,Stilo, Sorento, Nissan Livina , Porsche Cayenne, Toyota Corolla, Aston Martin, A8, Agile, idea, Strada, Frontier, Volvo C30, XC60, A4, x5, Tiggo, Linea <br>Lamborghini Gallardo, Tiida, Logan, Subaru Impreza, Z4, Chrysler 300C, Citroen C5, Palio, Tucson Sentra, Passion, Q7, Effa, M100, Doblo, Ranger, Iveco Daily, Panamera, Symbol, Suzuki SX4, A7, Ferrari California, Siena, Hyundai HR, Cherokee, Cadenz, Accord, Bongo, Land Rover Defender, 350z, Marc, Hoggar, Gol, Q5, X3, C4 Pallas, 458 Italia, Ecosport, Azera,Santa Fe, Outlander, 407, Master, Scenic, Ssangyong Actyon, Forester, Suzuki Jippe, Fox, A5, m5, Captiva, F430, Ducato, Land Rover Freelander, L200 Porsche 911, Smart Fortwo, Camry, Volvo, S60, S3, Celta, Classic, Montana, Prisma, Tracker, C4, Courier, Carens, Mohave, Cayman, Ssangyong Kyron, Suzuki Grand Vitara, RAV4, Omega, Fiesta Sedan, Partner , kangoo, Amarok, XC70, Aston Martin DBS, RS6, Blazer, S10, New Fiesta, CR0V, Land Rover Discovery, Countryman, 207 SW, 307, impreza WRX, Tribeca , Troller T4, S40, Martin DB9, RS5, Cielo Hatch, Vectra, Xsara Picasso , Effa Plutus, Weekend, Focus, Jaguar XF, Jeep Grand Cherokee, Carnival, Boxer, Boxster, Toyota Hilux SW4, Tiguan, XC90, TTS, Zafira, Mille, F0250, J3, C200, Classe B, Grand Livina, 307 CC, Megane, Actyon Sport, Legacy, Golf'
    body_final = tag_cleaner.cleanBody(body_raw)

    # countKeep = tag_cleaner.countKeep(body_tagg)
    # countDel = tag_cleaner.countDel(body_tagg)
    # countN = tag_cleaner.countN(body_tagg)

    print body_final

if __name__ == '__main__':
    run()
