from flask import Flask, request, render_template_string
from math import floor, ceil, log
import random
import sys
from fractions import Fraction


app = Flask(__name__)

#Za sezname O_m uporabimo quicksort in ker seznami |O_n|= n^2 hitro presežemo maksimalno rekurzijo zato malo povečajmo
sys.setrecursionlimit(2500)
#brez tega pridemo do 400(limita vgrajena v python je 1000), z povečano limito na 1500 pridemo do seznam_om(725), povečajmo na 2500 da dobimo seznam_om(1000), to je dovolj saj je velikosti miljon

def quicksort(sez):
    if len(sez) <= 1:
        return sez
    else:
        pivot = sez[0]
        leva = [x for x in sez[1:] if x < pivot]
        desna = [x for x in sez[1:] if x >= pivot]
        return quicksort(leva) + [pivot] + quicksort(desna)

#zahtevamo dolžino seznama n ter največjo števko v sezbnamu m
def gen_celo_st_sez_neurejen (n,m):
    seznam = []
    for i in range(0,n):
        seznam.append(random.randrange(1,m))

    return seznam

#uredimo zgornji seznam
def gen_celo_st_sez_urejen(n,m):
    return quicksort(gen_celo_st_sez_neurejen(n,m))

# tukaj seznam iz množice števil oblike O_m ={p/q; p,q \in {1,...,M}}, z vnosem n povemo koliko števil iz množice O_m želimo in z m označimo velikost M
#Še dodatna opomba, za seznam kot željen v članku želimo da m=n
def rand_gen_rac_sez (n,m):
    P = gen_celo_st_sez_neurejen(n,m)
    Q = gen_celo_st_sez_neurejen(n,m)
    Om = []
    for i in range(len(P)):
        Om.append(P[i]/Q[i])
    return quicksort(Om)


#NAČELOMA ŽELIM SEZNAM MNOŽICE OM Z VSEMI ŠTIVILI NE LE RANDOM GENERIRANI ELEMENTI

def seznam_om(m):
    Om = []
    for p in range(m):
        for q in range(m):
            Om.append(Fraction(p+1, q+1))
    return quicksort(Om)
    

M = [x for x in range(1,10+1)]
Om = seznam_om(10)

N = [x for x in range(1,100+1)]
On = seznam_om(100)

O = [x for x in range(1,1000+1)]

P = [x for x in range(1,10000+1)]

R = [x for x in range(1,100000+1)]

S = [x for x in range(1,1000000+1)]

Š = [x for x in range(1,10000000+1)]

#T = [x for x in range(1,100000000+1)]

# U = [x for x in range(1,1000000000+1)] # to je 10^9

# V = [x for x in range(1,10000000000+1)]

# Z = [x for x in range(1,100000000000+1)]

# Ž = [x for x in range(1,1000000000000+1)] # to je 10^12

#ŽŽ = [x for x in range(1,10000000000000+1)] # to je 10^13





#Oo = seznam_om(1000)



#Najprej predstavimo optimalno dvojiško iskanje za celo številske sezname


# def integer_part_pobiranje_iz_sez(sez):
   

# def integer_part_interval (n):
#     for i in range(10):
#         if n < 2**i:
#             return [2**(i-1),2**i]
#         else:
#             pass


#ta funkcija vzame seznam generiran od integer_part_interval npr [4,8] in naredi seznam [4,5,6,7,8]
def generiraj_seznam_od_do(sez):
    return [x for x in range(sez[0],sez[1]+1)]


#ni še vredu popravi, dela za vse razen za potence 2, da dejansk [16,16], n je lahko racionalno število vzamem le floor
def integer_part_interval(n):
    if n < 1:
        return ([[0,1]])
    else:
        i= 1
        seznam = [[0,1]]
        while i <= n:
            seznam.append(generiraj_seznam_od_do([i,2*i]))
            i = 2*i
        return seznam
    # return [x for x in range(2 ** (floor(log(floor(n))/log(2))),2**(ceil(log(floor(n))/log(2))))]



      

#to imenujemo binry search for integer in a list, vrne nam kolikokrat smovprašali ali je za večje ali manjše, če ejdemo število se ustavi ali ko ostane le ena številka


#Pazi, če smo z eksponentim iskanjem dobili interval dolžine 1, to funkcija nepotrbna sea imamo rešitev
#to imenujemo binry search for integer in a list, vrne nam kolikokrat smovprašali ali je za večje ali manjše, če ejdemo število se ustavi ali ko ostane le ena številka
#za n vzamemo celo število zato vzemimo floor od izbranega x 




def integer_part_solution_1(sez,n,i = None, sez_vseh_intervalov = None):
    #print("Vstopili smo v funkcijo")
    if i is None:
        i = 0
    if sez_vseh_intervalov is None:
        sez_vseh_intervalov = []

    if len(sez) == 0 :
        return (i, -1)
    min = sez[0]
    #print("min", min)
    max = sez[-1]
    #print("max", max)
    if len(sez) == 1:
        #print("Konec, ker je dolžina seznama 1")
        if min == n:
            sez_vseh_intervalov.append([n])
            return (i, sez_vseh_intervalov)
        else:
            return -1 #if number is not in a list
    if n == floor((max+min)/2):
        #print("Konec, ker smo zadeli število")
        sez_vseh_intervalov.append([n])
        return (i, sez_vseh_intervalov)
    elif floor((max+min)/2)  < n:
        sez1 = sez[sez.index(ceil((max+min)/2)):]
        #print("Vzeli smo drugo polovico", sez1)
        sez_vseh_intervalov.append(sez1)
        i += 1
        #print("število iteracije", i)
        return integer_part_solution_1(sez1,n,i,sez_vseh_intervalov)
        
    else:
        sez2 = sez[:sez.index(floor((max+min)/2)+1)]
        #tukaj vzamemo le prvo polovico lahko izločimo število, ki smo ga ugibali torej manj kot polovica, problem je če izberemo številko 0, ki ni vse znamu
        #bomo po korakih iteracije dobili [1,2], ugibamo da je številka 1 ampak to ni prav, zato vzamemo [], ker seznam prazeb se funkcija zruši.
        # Dve možni rešitvi lahko dodamo v seznam številko ki smo jo ugibali npr [1]( to naredimo tako: sez2 = sez[:sez.index(floor((max+min)/2)+1)]), 
        # Ali pa že tukaj preverimo ali je seznam prazen

        #print("Vzeli smo prvo polovico", sez2)
        sez_vseh_intervalov.append(sez2)
        i += 1
        #print("število iteracij", i)
        return integer_part_solution_1(sez2,n,i,sez_vseh_intervalov)
# Primer
# M = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# n = 2
# result = integer_part_solution_1(M, n)
# print(result)
    


#najdimo številke, ki da 
# največjo število iteracij in koliko iteraij je potrebno, damo seznam stevil vrne največiteracij potrebnih in 

def worst_case_for_int_za_vse(sez):
    max_iter = 0
    numb_with_worst_iter = []
    for i in range(len(sez)+1):
        iter = integer_part_solution_1(sez, i)
        if iter == max_iter:
            max_iter = iter
            numb_with_worst_iter.append(i)
        elif iter > max_iter:
            max_iter = iter
            numb_with_worst_iter=[i]
    return (max_iter, numb_with_worst_iter)

## tako napisana funkcija bo dala vedno najslabši rezultat za n = max(sez), tako da ni treba preveriti vseh števil
# torej za najslabšo iteracijo lahko preverimo, le največje število, ker ta funkcija se ustavi pri R 

def worst_case_for_int(sez):
    return integer_part_solution_1(sez, sez[-1])


#####Od tukaj naprejiščemo racinalni del, cel del smo že našli

#najprej dobimo ulomek oblike [mi/(2m^2),mi+1/2m^2], z navadnim binarnim iskanjem na intervalu [floor(x),floor(x)+1], našli smo že celi del x, zato lahko uporabimo floor(x) to že vemo,
#
# lower je našeni spodnji del, upper je naš zgornji del, x je točna številka iz Om ki jo ma odgovorjalec v mislih, M je omejitev Om z i štejmo korake iteracije, sez_vseh_intervalov
#binary_search_for_fraction(0,1,Fraction(1,81),100)
#dodaj še da izpisuje sezname, bi mogl bit čist lahko
def binary_search_for_fraction(lower,upper, x, M,i= None, seznam_vseh_intervalov = None):
    if i is None:
        i = 0
    if seznam_vseh_intervalov is None:
        seznam_vseh_intervalov = []
    if floor(x) == 0:
        m = M
    else:
        m = floor(M/ floor(x))
    if x <= (lower+ upper)/2:
        # torej x v prvi polovici intervala, treba preveriti ali interval že dovolj majhen
        #print( "Vzamemo prvo polovico intervala")
        seznam_vseh_intervalov.append([Fraction(lower), Fraction((lower+ upper)/2)])
        if (lower+ upper)/2 - lower < 1/(2*(m**2)):
            return ((Fraction(lower), Fraction((lower+ upper)/2)), i, seznam_vseh_intervalov)
        else:
            i += 1
            #print(i)
            return binary_search_for_fraction(Fraction(lower), Fraction((lower+ upper)/2), x, M, i, seznam_vseh_intervalov)
    else:
        # torej x v drugi polovici intervala, postopamo podobno
        #print( "Vzamemo drugo polovico intervala")
        seznam_vseh_intervalov.append([Fraction((lower+ upper)/2), Fraction(upper)])
        if  upper - (lower+ upper)/2 < 1/(2*(m**2)):
            return ((Fraction((lower+ upper)/2), Fraction(upper)), i, seznam_vseh_intervalov)
        else:
            i += 1
            #print(i)
            return binary_search_for_fraction(Fraction((lower+ upper)/2), Fraction(upper), x, M, i, seznam_vseh_intervalov)

#iteracije ne delajo  ne vem zakaj       
#Potrebno bo popraviti, da dejansko dobimo ulomek in ne racinalno število
        
# Za vizualno predstavo bom vrjetno potreboval tudi vse vmesne intervala naprintat al pa celo vrnit, to bom videl ko bom tam
        

# torej našli smo interval velikosti [mi/(2m^2),mi+1/2m^2] za nek mi.
# lema 4 nam pove da številka x v tem intervalu enolična. 
# Preostane nam samo še najti to število za to uporabimo postopek opisan v dokazu leme 5.
# kjer p7q predstavlja ulomek ki ga iščemo v seznamu




def find_fraction(a,b,c,d,p,q):
    if floor(a/b) == floor(c/d) and (a/b) == floor(a/b):
        U.append((a/b),(c/d))
        print(U)
        find_fraction(d,c % d,b,a %b,p - floor(a/b)*q,q)
    else:
        return (ceil(a/b),1)
    


def easysolution (a,b,c,d, M):
    for k in range(M):
        for j in range(M):
            if Fraction(a,b) <= (k+1)/(j+1) and  (k+1)/(j+1) <= Fraction(c,d):
                return Fraction(k+1,j+1)


#igralec izbere M
def generiraj_seznam(M):
    return seznam_om(M)

#igralec vzame x iz dobljenega seznama_om oblike Fraction(a,b) in M, ki ga je izbral že prej


#prva vrne vse sezname, ki jih preiščemo, druga pa le rešitev
def generiraj_vse_eks_sez_in_resitev(x,M):
    return (integer_part_interval(x), integer_part_interval(x)[-1])

#Prva pokaže celo bisekcijo, druga le rešitev
def gen_vse_sez_in_resi_za_celo_št_iskanje(x,M):
    return (integer_part_solution_1(generiraj_vse_eks_sez_in_resitev(x,M)[-1],floor(x))[-1],integer_part_solution_1(generiraj_vse_eks_sez_in_resitev(x,M)[-1],floor(x))[-1][-1])

#vrne vse intervale (torej interval vseh intervalo), zadnja le dvojec(ki predstavlja) interval prave velikosti prave velikosti
def najde_interval_za_rac_del(x,M):
    x = x - gen_vse_sez_in_resi_za_celo_št_iskanje(x,M)[-1][0]
    return (binary_search_for_fraction(gen_vse_sez_in_resi_za_celo_št_iskanje(x,M)[-1][0],  gen_vse_sez_in_resi_za_celo_št_iskanje(x,M)[-1][0] +1, x, M)[-1],
            binary_search_for_fraction(gen_vse_sez_in_resi_za_celo_št_iskanje(x,M)[-1][0],  gen_vse_sez_in_resi_za_celo_št_iskanje(x,M)[-1][0] +1, x, M)[0])

def najde_iskano_stevilko(x,M):
    return gen_vse_sez_in_resi_za_celo_št_iskanje(x,M)[-1][0] + easysolution(najde_interval_za_rac_del(x,M)[1][0].numerator, najde_interval_za_rac_del(x,M)[1][0].denominator, 
                                                                            najde_interval_za_rac_del(x,M)[1][1].numerator, najde_interval_za_rac_del(x,M)[1][1].denominator,M)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        M = int(request.form['number'])
        seznam = seznam_om(M)
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Generated List</title>
                <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
                <link href="{{ url_for('static', filename='css/styles.css') }}" rel="stylesheet">
            </head>
            <body>
                <div class="container">
                    <h1 class="text-center">Generated List</h1>
                    <p>List: [{{ seznam|join(', ') }}]</p>
                    <ul class="list-group">
                    {% for num in seznam %}
                        <li class="list-group-item"><a href="/number/{{ num }}">{{ num }}</a></li>
                    {% endfor %}
                    </ul>
                    <a class="btn btn-primary mt-3" href="/">Go back</a>
                </div>
            </body>
            </html>
        ''', seznam=seznam)
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Enter a Number</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
            <link href="{{ url_for('static', filename='css/styles.css') }}" rel="stylesheet">
        </head>
        <body>
            <div class="container">
                <h1 class="text-center">Enter a Number between 1 and 100</h1>
                <form method="post" class="form-inline justify-content-center">
                    <input type="number" class="form-control mb-2 mr-sm-2" name="number" min="1" max="100" required>
                    <button type="submit" class="btn btn-primary mb-2">Generate</button>
                </form>
            </div>
        </body>
        </html>
    ''')

@app.route('/number/<fraction>', methods=['GET'])
def display_number(fraction):
    M = 10 
    x = float(Fraction(fraction))
    intervals1 = generiraj_vse_eks_sez_in_resitev(x, M)[0]
    solution1 = generiraj_vse_eks_sez_in_resitev(x, M)[1]
    intervals2 = gen_vse_sez_in_resi_za_celo_št_iskanje(x, M)[0]
    solution2 = gen_vse_sez_in_resi_za_celo_št_iskanje(x, M)[1]
    interval3 = najde_interval_za_rac_del(x, M)[0]
    solution3 = najde_interval_za_rac_del(x, M)[1]
    final_solution = najde_iskano_stevilko(x, M)

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Selected Number</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
            <link href="{{ url_for('static', filename='css/styles.css') }}" rel="stylesheet">
        </head>
        <body>
            <div class="container">
                <h1 class="text-center">Selected Number: {{ fraction }}</h1>
                <div class="card">
                    <div class="card-body">
                        <h2>First Solution</h2>
                        <p>Intervals: {{ intervals1 }}</p>
                        <p>Solution: <span class="solution">{{ solution1 }}</span></p>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h2>Second Solution</h2>
                        <p>Intervals: {{ intervals2 }}</p>
                        <p>Solution: <span class="solution">{{ solution2 }}</span></p>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h2>Third Solution</h2>
                        <p>Intervals: {{ interval3 }}</p>
                        <p>Solution: <span class="solution">{{ solution3 }}</span></p>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h2>Final Solution</h2>
                        <p><span class="solution">{{ final_solution }}</span></p>
                    </div>
                </div>
                <a class="btn btn-primary mt-3" href="/">Go back</a>
            </div>
        </body>
        </html>
    ''', fraction=fraction, intervals1=intervals1, solution1=solution1, 
       intervals2=intervals2, solution2=solution2, interval3=interval3, 
       solution3=solution3, final_solution=final_solution)

if __name__ == '__main__':
    app.run(debug=True)