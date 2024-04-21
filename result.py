import PyPDF2
file=input()
result=0

# this part read information from pdf file and place 
# split pdf file in to two pages and extraxt page content to text variables
if file!="":
    try:        
        row=[]
        pdf_file=PyPDF2.PdfReader(open(file,"rb"))
        number_of_pages=len(pdf_file.pages)
        page1=pdf_file.pages[0]
        page2=pdf_file.pages[1]
        text1=page1.extract_text()
        text2=page2.extract_text()
        pos1 = text1.find("Apmaksai:")
        pos2 = text1.find("Elektroenerģijas patēriņš kopā")
        pos3 = text1.find("kWh")
        kopejaSumma = text1[pos1+10:pos2].rstrip()
        kopejaSumma = kopejaSumma.replace(",",".")
        row.append(kopejaSumma)
        pos4 = text2.find("Apjoms Mērv. Cena,")
        periods1 = text2[pos4-23:pos4-13]
        vertiba1=periods1[6:10]+'-'+periods1[3:5]+'-'+periods1[0:2]
        gads1=periods1[6:10]
        menesis1=periods1[3:5]
        row.append(vertiba1)
        periods2 = text2[pos4-10:pos4]
        vertiba2=periods2[6:10]+'-'+periods2[3:5]+'-'+periods2[0:2]
        row.append(vertiba2)
        paterins = text1[pos2+32:pos3]
        paterins = paterins.replace(",",".")
        paterins = paterins.replace(" ","")
        row.append(paterins)
        pos3=text2.find("kWh")
        cena = text2[pos3+4:pos3+10].rstrip()
        cena = cena.replace(",",".")
        row.append(cena)
        data=[]
         # this part
        with open("nordpool.csv","r") as f:
            next(f)
            for line in f:
                x=line.rstrip().split(",")
                y=x[0].split(" ")
                z=y[0].split("-")
                if(z[0]==gads1 and z[1]==menesis1):
                    data.append(float(x[2]))
        birzasCena=sum(data)/(len(data))
        birzasSumma=round(birzasCena,3)*round(float(paterins),3)
        fiksetaSumma=float(cena)*round(float(paterins),3)
        fiksetaSumma=round(fiksetaSumma,3)
        birzasSumma=round(birzasSumma,3)
        result=fiksetaSumma-birzasSumma
        result=round(result, 1)
        if(result==0.0):
            result=0
        print(result)
    except FileNotFoundError:
        print(0)


    


