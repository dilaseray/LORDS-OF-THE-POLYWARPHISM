import pygame

import sys

import random

num_kordi=dict()

kordi_num=dict()

renkler={"red":(255,0,0),"blue":(51,51,255),"green":(51,255,51),"yellow":(255,255,153),"black":(0,0,0),"white":(255,255,255)}

class Muhafız():
    
    def __init__(self,isim,numara,renk,player):
        self.can=80

        self.kaynak=10

        self.player=player

        self.numara=numara

        self.komsular = []

        self.saldırma_menzili=[]

        self.SetBolgeRenk(renk)

        karerenkdegistir(screen,renk,self.numara,isim,self.player,can=self.can,kaynak=self.kaynak)

        self.yerlesme_menzil()

        self.saldırma_menzil()
       
    def SetBolgeRenk(self,renk):
        
        self.renk=renk
    
    def yerlesme_menzil(self):
        
        satir = (self.numara - 1) // cols

        sutun = (self.numara - 1) % rows

        for x in range(max(0, satir - 1), min(satir + 2, len(oyunmatrisi))):

            for y in range(max(0, sutun - 1), min(sutun + 2, len(oyunmatrisi[0]))):

                if (x, y) != (satir, sutun):

                    satir=satirokuyucu("game.txt",oyunmatrisi[x][y]).split("*")

                    if satir[2]=="." and satir[1]=="black" :

                        self.komsular.append(oyunmatrisi[x][y])
                        
        for hucre in self.komsular:
        
            karerenkdegistir(screen,self.renk,hucre,".",self.player)

        return self.komsular

    def imha(self):

        karerenkdegistir(screen,"black",self.numara,".")

        for hucre in self.komsular:
            
            durum=satirokuyucu("game.txt",hucre).split("*")

            if durum[2]==".":

                karerenkdegistir(screen,"black",hucre,".")

    def saldırma_menzil(self):

        satir = (self.numara - 1) // rows

        sutun = (self.numara - 1) % cols

        for x in range(max(0, satir - 1), min(satir + 2, len(oyunmatrisi))):

            for y in range(max(0, sutun - 1), min(sutun + 2, len(oyunmatrisi[0]))):

                if (x, y) != (satir, sutun):

                    self.saldırma_menzili.append(oyunmatrisi[x][y])
    
    def bilgiguncelle(self):

        durum=satirokuyucu("game.txt",self.numara).split("*")

        self.can=float(durum[4])

    def saldir(self):
       
       for i in self.saldırma_menzili:
           
           dusman=satirokuyucu("game.txt",i).split("*")

           if dusman[1]!=self.renk and  dusman[2]!=".":
               
               bilgi=str(dusman[0])+"*"+dusman[1]+"*"+dusman[2]+"*"+dusman[3]+"*"+str(float(dusman[4])-20)

               satiryazici("game.txt",i,bilgi)
               
class Okcu(Muhafız):
    
    def saldırma_menzil(self):
        
        boyut = len(oyunmatrisi)

        satir = (self.numara - 1) // boyut

        sutun = (self.numara - 1) % boyut
        
        self.saldırma_menzili = []

        if satir+1<boyut and sutun+1<boyut:

            self.saldırma_menzili.append(oyunmatrisi[satir+1][sutun+1])

        if satir+2<boyut and sutun+2<boyut:

            self.saldırma_menzili.append(oyunmatrisi[satir+2][sutun+2])

        if satir-1>=0 and sutun+1<boyut:

            self.saldırma_menzili.append(oyunmatrisi[satir-1][sutun+1]) 

        if satir-2>=0 and sutun+2<boyut:

            self.saldırma_menzili.append(oyunmatrisi[satir-2][sutun+2])

        if satir-1>=0 and sutun-1>=0:

            self.saldırma_menzili.append(oyunmatrisi[satir-1][sutun-1])

        if satir+1<boyut and sutun-1>=0:

            self.saldırma_menzili.append(oyunmatrisi[satir+1][sutun-1])

        if satir-2>=0 and sutun-2>=0:

            self.saldırma_menzili.append(oyunmatrisi[satir-2][sutun-2])

        if satir+2<boyut and sutun-2>=0:

            self.saldırma_menzili.append(oyunmatrisi[satir+2][sutun-2])   
        
        satir = (self.numara - 1) // boyut

        sutun = (self.numara - 1) % boyut
            
        for x in range(max(0, satir - 2), min(boyut, satir + 3)):

            for y in range(max(0, sutun - 2), min(boyut, sutun + 3)):
                    # Geçerli indekslerin sınırlarını kontrol et ve sadece sağ, sol, yukarı ve aşağı hücreleri al
                if (x, y) != (satir, sutun) and (x == satir or y == sutun):

                    self.saldırma_menzili.append(oyunmatrisi[x][y])
       
    def SetBolgeRenk(self,renk):

        self.can=30

        self.kaynak=20

        self.renk=renk    

    def saldir(self):
        
        saldirilacak=[]

        for i in self.saldırma_menzili:

            dusman=satirokuyucu("game.txt",i).split("*")

            if dusman[1]!=self.renk and dusman[2]!=".":

                saldirilacak.append(dusman)

        saldirilacak=sorted(saldirilacak, key=lambda x: x[-2], reverse=True)

        if len(saldirilacak)<=3:

            for i in range(len(saldirilacak)):

                can=float(saldirilacak[i][4])-float(float(saldirilacak[i][4])*(60/100))

                bilgi=str(saldirilacak[i][0])+"*"+saldirilacak[i][1]+"*"+saldirilacak[i][2]+"*"+saldirilacak[i][3]+"*"+str(can)

                satiryazici("game.txt",int(saldirilacak[i][0]),bilgi)

        else:

            for i in range(3):
                
                can=float(saldirilacak[i][4])-float(float(saldirilacak[i][4])*(60/100))

                bilgi=str(saldirilacak[i][0])+"*"+saldirilacak[i][1]+"*"+saldirilacak[i][2]+"*"+saldirilacak[i][3]+"*"+str(can)

                satiryazici("game.txt",int(saldirilacak[i][0]),bilgi)

class Topcu(Muhafız):

    def saldırma_menzil(self):
        
        boyut = len(oyunmatrisi)
        # Numaranın indekslerini bul
        satir = (self.numara - 1) // boyut

        sutun = (self.numara - 1) % boyut
        
        for x in range(max(0, satir - 2), min(boyut, satir + 3)):

            for y in range(max(0, sutun - 2), min(boyut, sutun + 3)):
                # Geçerli indekslerin sınırlarını kontrol et ve sadece sağ, sol, yukarı ve aşağı hücreleri al
                if (x, y) != (satir, sutun) and (x == satir or y == sutun):

                    self.saldırma_menzili.append(oyunmatrisi[x][y])

    def SetBolgeRenk(self,renk):

        self.can=30

        self.kaynak=50

        self.renk=renk 

    def saldir(self):

        saldirilacak=[]

        for i in self.saldırma_menzili:

            dusman=satirokuyucu("game.txt",i).split("*")

            if dusman[1]!=self.renk and dusman[2]!=".":

                saldirilacak.append(dusman)

        saldirilacak=sorted(saldirilacak, key=lambda x: x[-2], reverse=True)

        can=0

        bilgi=str(saldirilacak[0][0])+"*"+saldirilacak[0][1]+"*"+saldirilacak[0][2]+"*"+saldirilacak[0][3]+"*"+str(can)

        satiryazici("game.txt",int(saldirilacak[0][0]),bilgi)

class Atlı(Muhafız):

    def saldırma_menzil(self):
        
        boyut = len(oyunmatrisi)

        satir = (self.numara - 1) // boyut

        sutun = (self.numara - 1) % boyut
        
        if satir+1<boyut and sutun+1<boyut:

            self.saldırma_menzili.append(oyunmatrisi[satir+1][sutun+1])

        if satir+2<boyut and sutun+2<boyut:

            self.saldırma_menzili.append(oyunmatrisi[satir+2][sutun+2])

        if satir-1>=0 and sutun+1<boyut:

            self.saldırma_menzili.append(oyunmatrisi[satir-1][sutun+1]) 

        if satir-2>=0 and sutun+2<boyut:

            self.saldırma_menzili.append(oyunmatrisi[satir-2][sutun+2])

        if satir-1>=0 and sutun-1>=0:

            self.saldırma_menzili.append(oyunmatrisi[satir-1][sutun-1])

        if satir+1<boyut and sutun-1>=0:

            self.saldırma_menzili.append(oyunmatrisi[satir+1][sutun-1])

        if satir-2>=0 and sutun-2>=0:

            self.saldırma_menzili.append(oyunmatrisi[satir-2][sutun-2])

        if satir+2<boyut and sutun-2>=0:

            self.saldırma_menzili.append(oyunmatrisi[satir+2][sutun-2])   

        if satir-3>=0 and sutun-3>=0:

            self.saldırma_menzili.append(oyunmatrisi[satir-3][sutun-3])

        if satir+3 <boyut and sutun+3<boyut:

            self.saldırma_menzili.append(oyunmatrisi[satir+3][sutun+3])

        if satir+3<boyut and sutun-3>=0:

            self.saldırma_menzili.append(oyunmatrisi[satir+3][sutun-3])

        if satir-3>=0 and sutun+3 <boyut:

            self.saldırma_menzili.append(oyunmatrisi[satir-3][sutun+3])

    def SetBolgeRenk(self,renk):

        self.can=40

        self.kaynak=30

        self.renk=renk 

    def saldir(self):

        saldirilacak=[]

        for i in self.saldırma_menzili:

            dusman=satirokuyucu("game.txt",i).split("*")

            if dusman[1]!=self.renk and dusman[2]!=".":

                saldirilacak.append(dusman)
        
        saldirilacak=sorted(saldirilacak, key=lambda x: x[-1], reverse=True)

        if len(saldirilacak)<=3:

            for i in range(len(saldirilacak)):

                can=float(saldirilacak[i][4])-float(30)

                bilgi=str(saldirilacak[i][0])+"*"+saldirilacak[i][1]+"*"+saldirilacak[i][2]+"*"+saldirilacak[i][3]+"*"+str(can)

                satiryazici("game.txt",int(saldirilacak[i][0]),bilgi)

        else:

            for i in range(3):
                
                can=float(saldirilacak[i][4])-float(30)

                bilgi=str(saldirilacak[i][0])+"*"+saldirilacak[i][1]+"*"+saldirilacak[i][2]+"*"+saldirilacak[i][3]+"*"+str(can)

                satiryazici("game.txt",int(saldirilacak[i][0]),bilgi)

class Saglıkcı(Muhafız):

    def saldırma_menzil(self):
        
        boyut = len(oyunmatrisi)

        satir = (self.numara - 1) // boyut

        sutun = (self.numara - 1) % boyut
        
        self.saldırma_menzili = []

        if satir+1<boyut and sutun+1<boyut:

            self.saldırma_menzili.append(oyunmatrisi[satir+1][sutun+1])

        if satir+2<boyut and sutun+2<boyut:

            self.saldırma_menzili.append(oyunmatrisi[satir+2][sutun+2])

        if satir-1>=0 and sutun+1<boyut:

            self.saldırma_menzili.append(oyunmatrisi[satir-1][sutun+1]) 

        if satir-2>=0 and sutun+2<boyut:

            self.saldırma_menzili.append(oyunmatrisi[satir-2][sutun+2])

        if satir-1>=0 and sutun-1>=0:

            self.saldırma_menzili.append(oyunmatrisi[satir-1][sutun-1])

        if satir+1<boyut and sutun-1>=0:

            self.saldırma_menzili.append(oyunmatrisi[satir+1][sutun-1])

        if satir-2>=0 and sutun-2>=0:

            self.saldırma_menzili.append(oyunmatrisi[satir-2][sutun-2])

        if satir+2<boyut and sutun-2>=0:
            
            self.saldırma_menzili.append(oyunmatrisi[satir+2][sutun-2])   
        
        satir = (self.numara - 1) // boyut

        sutun = (self.numara - 1) % boyut
            
        for x in range(max(0, satir - 2), min(boyut, satir + 3)):

            for y in range(max(0, sutun - 2), min(boyut, sutun + 3)):
                    # Geçerli indekslerin sınırlarını kontrol et ve sadece sağ, sol, yukarı ve aşağı hücreleri al
                if (x, y) != (satir, sutun) and (x == satir or y == sutun):

                    self.saldırma_menzili.append(oyunmatrisi[x][y])

    def SetBolgeRenk(self,renk):

        self.can=100

        self.kaynak=10

        self.renk=renk 

    def saldir(self):

        iyilestiricek=[]

        for i in self.saldırma_menzili:

            dost=satirokuyucu("game.txt",i).split("*")

            if dost[1]==self.renk and dost[2]!=".":

                iyilestiricek.append(dost)

        iyilestiricek=sorted(iyilestiricek, key=lambda x: x[-2], reverse=False)

        if len(iyilestiricek)<=3:

            for i in range(len(iyilestiricek)):

                can=float(iyilestiricek[i][4])+float(float(iyilestiricek[i][4])*(50/100))

                bilgi=str(iyilestiricek[i][0])+"*"+iyilestiricek[i][1]+"*"+iyilestiricek[i][2]+"*"+iyilestiricek[i][3]+"*"+str(can)

                satiryazici("game.txt",int(iyilestiricek[i][0]),bilgi)

        else:

            for i in range(3):
                
                can=float(iyilestiricek[i][4])+float(float(iyilestiricek[i][4])*(50/100))

                bilgi=str(iyilestiricek[i][0])+"*"+iyilestiricek[i][1]+"*"+iyilestiricek[i][2]+"*"+iyilestiricek[i][3]+"*"+str(can)

                satiryazici("game.txt",int(iyilestiricek[i][0]),bilgi)

hak=0
class Oyuncu():

    def __init__(self,oyuncu,renk,no):

        self.no=no

        self.devamdurumu=True

        self.anliksaldirikarakter=[]

        self.hazine=200

        self.oyuncu=oyuncu

        self.renk=renk

        self.oyunmatrisi=oyunmatrisi
        
        self.karakterlist=[]

        self.muhafızsay=1

        self.okcusay=0
        
        self.saglikcisay=0

        self.atlısay=0

        self.topcusay=0

        self.startgame()

        self.etkin_alan_numaraları=[]

        self.pas=0

    def cankontrol(self):

        indx=0

        for i in self.karakterlist:
           
           i.bilgiguncelle()

           if i.can<=0:
               
               i.imha()

               self.karakterlist.pop(indx)
               
        indx+=1

    def startgame(self):

        nesne=Muhafız("M1",self.no,self.renk,self.oyuncu)

        self.karakterlist.append(nesne)

    def toplam_alan(self):

        self.etkin_alan_numaraları=[]

        for i in range(1,cols*rows):

            hucre=satirokuyucu("game.txt",i).split("*")
            
            if  hucre[2]=="." and hucre[1]==self.renk:
               
                self.etkin_alan_numaraları.append(int(hucre[0]))

    def diskalifiye(self):

        if self.pas==3:

            self.devamdurumu=False

            self.imha()

    def imha(self):

        for i in self.karakterlist:
            i.bilgiguncelle()
            i.imha()

        self.toplam_alan()

    def saldiriyap(self):
        
        for i in self.anliksaldirikarakter:
            
            i.saldir()
            
        self.anliksaldirikarakter=[]

    def karakter_ekle(self,karakterkodu,kordinatno):

        global hak

        if karakterkodu=="1" and  (kordinatno in self.etkin_alan_numaraları):

            hak+=1

            self.atlısay+=1

            nesne=Atlı("A"+str(self.atlısay),kordinatno,self.renk,self.oyuncu)

            self.karakterlist.append(nesne)

            self.anliksaldirikarakter.append(nesne)

        if karakterkodu=="2" and  (kordinatno in self.etkin_alan_numaraları):
            hak+=1

            self.muhafızsay+=1

            nesne=Muhafız("M"+str(self.muhafızsay),kordinatno,self.renk,self.oyuncu)

            self.karakterlist.append(nesne)

            self.anliksaldirikarakter.append(nesne)

        if karakterkodu=="3" and  (kordinatno in self.etkin_alan_numaraları):

            hak+=1

            self.okcusay+=1

            nesne=Okcu("O"+str(self.okcusay),kordinatno,self.renk,self.oyuncu)

            self.karakterlist.append(nesne)

            self.anliksaldirikarakter.append(nesne)

        if karakterkodu=="4" and  (kordinatno in self.etkin_alan_numaraları):

            hak+=1

            self.saglikcisay+=1

            nesne=Saglıkcı("S"+str(self.saglikcisay),kordinatno,self.renk,self.oyuncu)

            self.karakterlist.append(nesne)

            self.anliksaldirikarakter.append(nesne)

        if karakterkodu=="5" and  (kordinatno in self.etkin_alan_numaraları):

            hak+=1

            self.topcusay+=1

            nesne=Topcu("T"+str(self.topcusay),kordinatno,self.renk,self.oyuncu)

            self.karakterlist.append(nesne)

            self.anliksaldirikarakter.append(nesne)
        
pygame.init() # Modül etkinleştirme

SQUARE_SIZE = 40 # Kare boyutu

nokta_font = pygame.font.SysFont("arial", 20) # Nokta yazı fontu
      
clock = pygame.time.Clock() # Oyun saati etkinleştirme

def matris_olustur(satir_sayisi, sutun_sayisi):

    matris = []

    sayac = 1

    for x1 in range(satir_sayisi):

        satir = []

        for x2 in range(sutun_sayisi):

            satir.append(sayac)

            sayac += 1

        matris.append(satir)

    return matris

def satirokuyucu(file,satır):

    dosya=open(file,"r",encoding="utf-8")

    for i in range(satır-1):

        dosya.readline()
    
    satırverisi=dosya.readline().strip("\n")
    
    dosya.close()

    return satırverisi

def satiryazici(dosya_adı, satir, veri):
 
    with open(dosya_adı, "r",encoding="utf-8") as file:

        lines = file.readlines()
     
    lines[satir - 1] = veri + "\n" 

    with open(dosya_adı, "w",encoding="utf-8") as file:

        file.writelines(lines)

def draw_grid(screen, rows, cols,dosya):
    
    size=1

    for row in range(rows):

        for col in range(cols):
            
            xkord = col * SQUARE_SIZE

            ykord = row * SQUARE_SIZE

            noktatext = nokta_font.render(".", True, renkler["white"])

            text_rect = noktatext.get_rect(center=(xkord + SQUARE_SIZE // 2, ykord + SQUARE_SIZE // 2))

            pygame.draw.rect(screen, renkler["white"], (xkord, ykord, SQUARE_SIZE, SQUARE_SIZE),1)

            screen.blit(noktatext, text_rect)

            num_kordi[size]=(xkord,ykord)
            kordi_num[(xkord,ykord)]=size
            size+=1

    pygame.display.flip()  # Ekranı güncelle

    with open(dosya,"w",encoding="utf-8")as kayit:
    
        for konum in range(1,rows*cols+1):

            bilgi="{}*black*.*Unkown\n".format(konum)

            kayit.write(bilgi)

def karerenkdegistir(ekran, rengi, sira,isim,sahip="Unkown",can=0,kaynak=0): # numara*renk*kareyazı*sahip*can formatı

    noktatext = nokta_font.render(isim, True, renkler["black"])

    pygame.draw.rect(ekran,renkler[rengi],(num_kordi[sira][0],num_kordi[sira][1],SQUARE_SIZE,SQUARE_SIZE))

    text_rect = noktatext.get_rect(center=(num_kordi[sira][0] + SQUARE_SIZE // 2, num_kordi[sira][1] + SQUARE_SIZE // 2))

    screen.blit(noktatext, text_rect)

    pygame.draw.rect(ekran,renkler["white"],(num_kordi[sira][0],num_kordi[sira][1],SQUARE_SIZE,SQUARE_SIZE),1)

    pygame.display.flip()  # Ekranı güncelle

    bilgi=str(sira)+"*"+rengi+"*"+isim+"*"+sahip+"*"+str(can)+"*"+str(kaynak)

    satiryazici("game.txt",sira,bilgi)
    
def mouse_target():
    
    for i in num_kordi.values():

        mouse_xx, mouse_yy = pygame.mouse.get_pos()

        if i[0]<mouse_xx<i[0]+40 and i[1]<mouse_yy <i[1]+40 :

            return kordi_num[(i[0],i[1])]
        
boyut = input("Boyutu giriniz (AxB şeklinde): ").split("x") # Kullanıcıdan boyut bilgisi al

rows = int(boyut[0])

cols = int(boyut[1])

oyunmatrisi=matris_olustur(rows,cols)

width = cols * SQUARE_SIZE+220

height = rows * SQUARE_SIZE

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("LORDS OF THE POLYWARPHISM")

screen.fill(renkler["black"])  # Ekranı siyahla doldurun

draw_grid(screen, rows, cols,"game.txt")  # Kareleri çizin

koseno=[oyunmatrisi[0][0],oyunmatrisi[len(oyunmatrisi)-1][len(oyunmatrisi)-1],oyunmatrisi[0][len(oyunmatrisi)-1],oyunmatrisi[len(oyunmatrisi)-1][0]]

numbers = [0, 1, 2, 3]

random.shuffle(numbers)  # Sayıları karıştır

p1=Oyuncu("player1","red", koseno[numbers[0]])

p2=Oyuncu("player2","blue", koseno[numbers[1]])

p3=Oyuncu("player3","green",koseno[numbers[2]])

p4=Oyuncu("player4","yellow",koseno[numbers[3]])

sıra=[p1,p2,p3,p4,"saldiri"]   # Oyuncular

index=0

font = pygame.font.SysFont(None, 20)

while True:
    # Olayları işle
    mevcutOyuncu=sıra[index]

    if  not mevcutOyuncu=="saldiri":

        textsıra=font.render("sıra {}({})".format(mevcutOyuncu.oyuncu,mevcutOyuncu.renk),True,renkler["white"])

    else:
        textsıra=font.render("sıra {}".format("saldiri"),True,renkler["white"])

    pygame.draw.rect(screen,renkler["black"],(height,40,height+30,50))

    screen.blit(textsıra,(height+30, 50))
    
    if mevcutOyuncu=="saldiri":
        
        for i in sıra[:len(sıra)-1]:

            i.saldiriyap()
            
        for i in sıra[:len(sıra)-1]:

            i.cankontrol()

            i.toplam_alan()

        index = (index + 1) % len(sıra)

    else:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                sys.exit()

            elif event.type == pygame.KEYDOWN:
                # Klavye tuşlarını işle
                if event.key == pygame.K_1 and hak<2:

                    klavyeno="1"

                    mauseno=mouse_target()

                    mevcutOyuncu.toplam_alan()

                    mevcutOyuncu.karakter_ekle(klavyeno,mauseno)
                    
                elif event.key == pygame.K_2 and hak<2:

                    klavyeno="2"

                    mauseno=mouse_target()

                    mevcutOyuncu.toplam_alan()

                    mevcutOyuncu.karakter_ekle(klavyeno,mauseno)
                                
                elif event.key == pygame.K_3 and hak<2:

                    klavyeno="3"

                    mauseno=mouse_target()

                    mevcutOyuncu.toplam_alan()

                    mevcutOyuncu.karakter_ekle(klavyeno,mauseno)
                    
                elif event.key == pygame.K_4 and hak<2:

                    klavyeno="4"

                    mauseno=mouse_target()

                    mevcutOyuncu.toplam_alan()

                    mevcutOyuncu.karakter_ekle(klavyeno,mauseno)
                    
                elif event.key == pygame.K_5 and hak<2:

                    klavyeno="5"

                    mauseno=mouse_target()

                    mevcutOyuncu.toplam_alan()

                    mevcutOyuncu.karakter_ekle(klavyeno,mauseno)

                elif not hak<2 :

                    hak=0

                    index = (index + 1) % len(sıra)

                elif event.key==pygame.K_q:

                    mevcutOyuncu.pas+=1

                    index = (index + 1) % len(sıra)
            
        if not mevcutOyuncu=="saldiri":

            mevcutOyuncu.diskalifiye()

        



    mouse_x, mouse_y = pygame.mouse.get_pos()
      
    mouse_click = pygame.mouse.get_pressed()  

    pygame.draw.rect(screen,renkler["black"],(height,20,height+20,20))
    text = font.render(f"Fare Pozisyonu: ({mouse_x}, {mouse_y})", True, renkler["white"])

    screen.blit(text, (height+30, 20))
       
    pygame.display.flip()

    clock.tick(15)