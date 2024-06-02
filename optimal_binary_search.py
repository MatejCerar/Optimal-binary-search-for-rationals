from flask import Flask, request, render_template_string, url_for
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

#Oo = seznam_om(1000)





#ta funkcija vzame seznam generiran od integer_part_interval npr [4,8] in naredi seznam [4,5,6,7,8]
def generiraj_seznam_od_do(sez):
    return [x for x in range(sez[0],sez[1]+1)]




#Najprej predstavimo optimalno dvojiško iskanje za celo številske sezname

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
   


      

#Naslednjo funkcijo imenujemo binary search for integer in a list, vrne nam kolikokrat smo vprašali ali je naša številka večje ali manjše, če najdemo število se ustavi ali ko ostane le ena številka


#Pazi, če smo z eksponentim iskanjem dobili interval dolžine 1, to funkcija nepotrebna saj imamo rešitev

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
  
# Za vizualno predstavo bom vrjetno potreboval tudi vse vmesne intervala naprintat al pa celo vrnit, to bom videl ko bom tam


#zopet za najslabši primer tukaj gledamo le elemente iz seznam od 0 do 1, najslabše se bo vedel zadnji element v seznamu
def worst_case_for_rationals(M):
    Om_do_1 = []
    for p in range(M):
        for q in range(p,M):
            Om_do_1.append(Fraction(p+1, q+1))
    sez = quicksort(Om_do_1)
    return binary_search_for_fraction(0,1, sez[-1], M)
    
    

# torej našli smo interval velikosti [mi/(2m^2),mi+1/2m^2] za nek mi.
# lema 4 nam pove da številka x v tem intervalu enolična. 
# Preostane nam samo še najti to število za to uporabimo postopek opisan v dokazu leme 5.

    
def find_fraction(a, b, c, d):
    if floor(a/b) == floor(c/d) and (a / b) % 1 != 0:  # Case 1
        b_, aa = find_fraction(d, c % d, b, a % b)
        #print( b_, aa)
        a_ = floor(a/b) * b_ + aa
        return Fraction(a_, b_)
    else:  # Case 2
        return ceil(a/b), 1



def easysolution (a,b,c,d, M):
    for k in range(M):
        for j in range(M):
            if Fraction(a,b) <= (k)/(j+1) and  (k)/(j+1) <= Fraction(c,d):
                return Fraction(k,j+1)



#Poglejmo nekaj najslabsih primerov za binarno iskanje celega števila:
def whole_nm_eorst_case(M):
    sez = [0]
    for i in range(1,M+1):
        sez1 = [x for x in range(1,i+1)]
        w = worst_case_for_int(sez1)[0]
        if w != sez[-1]:
            sez.append(worst_case_for_int(sez1)[0])
    return sez

def rationa_nm_worst_case(M):
    sez = [0]
    for i in range(1,M+1):
        w = worst_case_for_rationals(sez)[1]
        if worst_case_for_rationals(sez)[1] != sez[-1]:
            sez.append(worst_case_for_rationals(sez)[0])
    return sez




#VSE FUNKCIJE SKUPAJ


#igralec izbere M
def generiraj_seznam(M):
    return seznam_om(M)

#igralec vzame x iz dobljenega seznama_om oblike Fraction(a,b) in M, ki ga je izbral že prej
#Primer1 (Fraction(1,7), 10)
#Primer2 (Fraction(4), 5)

#prva vrne vse sezname, ki jih preiščemo (vrne seznam seznamov npr [[0,1],[1,2],[2,4]]), druga pa le rešitev seznam npr [2,4]
def generiraj_vse_eks_sez_in_resitev(x,M):
    return (integer_part_interval(x), integer_part_interval(x)[-1])

#Prva pokaže celo bisekcijo (vrne seznam seznamov), druga le rešitev seznam v katerem rešitrv npr [0]
def gen_vse_sez_in_resi_za_celo_št_iskanje(x,M):
    return (integer_part_solution_1(generiraj_vse_eks_sez_in_resitev(x,M)[-1],floor(x))[-1],integer_part_solution_1(generiraj_vse_eks_sez_in_resitev(x,M)[-1],floor(x))[-1][-1])

#vrne vse intervale (torej interval vseh intervalov npr [[Fraction(0, 1), Fraction(1, 2)], [Fraction(0, 1), Fraction(1, 4)], [Fraction(1, 8), Fraction(1, 4)], [Fraction(1, 8), Fraction(3, 16)], 
#                                                         [Fraction(1, 8), Fraction(5, 32)], [Fraction(9, 64), Fraction(5, 32)], [Fraction(9, 64), Fraction(19, 128)], 
#                                                         [Fraction(9, 64), Fraction(37, 256)]]), 
# zadnja vrne le dvojec(ki predstavlja) interval prave velikosti npr (Fraction(9, 64), Fraction(37, 256))
def najde_interval_za_rac_del(x,M):
    return (binary_search_for_fraction(gen_vse_sez_in_resi_za_celo_št_iskanje(x,M)[-1][0],  gen_vse_sez_in_resi_za_celo_št_iskanje(x,M)[-1][0] +1, x, M)[-1],
            binary_search_for_fraction(gen_vse_sez_in_resi_za_celo_št_iskanje(x,M)[-1][0],  gen_vse_sez_in_resi_za_celo_št_iskanje(x,M)[-1][0] +1, x, M)[0])

#Vrne iskano število
def najde_iskano_stevilko(x,M):
    if najde_interval_za_rac_del(x,M)[-1][1].numerator == 1 and najde_interval_za_rac_del(x,M)[-1][1].denominator == 1 :
        return gen_vse_sez_in_resi_za_celo_št_iskanje(x,M)[-1][0]
    else:
        return find_fraction(najde_interval_za_rac_del(x,M)[-1][0].numerator, najde_interval_za_rac_del(x,M)[-1][0].denominator, 
                      najde_interval_za_rac_del(x,M)[-1][1].numerator, najde_interval_za_rac_del(x,M)[-1][1].denominator)


@app.route('/', methods=['GET'])
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Optimal search for rationals</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container">
                <h1 class="text-center">Enter a Number between 1 and 100</h1>
                <form method="post" action="{{ url_for('generate') }}" class="form-inline justify-content-center">
                    <input type="number" class="form-control mb-2 mr-sm-2" name="number" min="1" max="100" required>
                    <button type="submit" class="btn btn-primary mb-2">Generate</button>
                </form>
            </div>
            <div>      
            <h4>
                 Here one can try out the optimal algorihm for searching a rational number in the set of type p/q where p and q natural numbers of size at most your chosen number. 
                 So firstly you choose any natural number. This will generate list as described above. Then you will choose any number from the generated set and the sloution for steps taken by algorithm will apear.
            </h4>          
            </div>
        </body>
        </html>
    ''')

@app.route('/generate', methods=['POST'])
def generate():
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
        </head>
        <body>
            <h4>
                 Choose any number from the list
            </h4>   
            <div class="container">
                <h1 class="text-center">Generated List</h1>
                <p>List: [</p>
                <div class="d-flex flex-wrap">
                    {% for num in seznam %}
                        <form method="post" action="{{ url_for('display_number') }}" class="mr-2 mb-2">
                            <input type="hidden" name="fraction" value="{{ num }}">
                            <button type="submit" class="btn btn-link">{{ num }}</button>
                        </form>
                        {% if not loop.last %}, {% endif %}
                    {% endfor %}
                </div>
                <p>]</p>
                <a class="btn btn-primary mt-3" href="/">Go back</a>
            </div>
        </body>
        </html>
    ''', seznam=seznam)



        # TA DEL KODE JE ČE ŽELIM IMETI ELEMENTE SEZNAMA V VRSTICH ZA KLIKAT, TOREJ NAJPREJ LE NAPIŠE SEZNAM NATO PA ŠE V VSAKI VRSTICI ENA ŠTEVILKE ZA KLIKNIT, MENI LJUBŠA ZGORNJA VERZIJA
        # <body>
        #     <div class="container">
        #         <h1 class="text-center">Generated List</h1>
        #         <p>List: [{{ seznam|join(', ') }}]</p>
        #         <ul class="list-group">
        #         {% for num in seznam %}
        #             <li class="list-group-item">
        #                 <form method="post" action="{{ url_for('display_number') }}">
        #                     <input type="hidden" name="fraction" value="{{ num }}">
        #                     <button type="submit" class="btn btn-link">{{ num }}</button>
        #                 </form>
        #             </li>
        #         {% endfor %}
        #         </ul>
        #         <a class="btn btn-primary mt-3" href="/">Go back</a>
        #     </div>
        # </body>

@app.route('/display_number', methods=['POST'])
def display_number():
    fraction = request.form['fraction']
    fraction = Fraction(fraction)
    M = 10  
    x = float(fraction)
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
            <title>Optimal search for rationals</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container">
                <h1 class="text-center">Selected Number: {{ fraction }}</h1>
                <div class="card">
                    <div class="card-body">
                        <h2>Solution for exponential search</h2>
                        <p>Intervals: {{ intervals1 }}</p>
                        <p>Solution: <span class="solution">{{ solution1 }}</span></p>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h2>Solution for optimal binary search for whole numbers</h2>
                        <p>Intervals: {{ intervals2 }}</p>
                        <p>Solution: <span class="solution">{{ solution2 }}</span></p>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h2>Solution for the interva containig exactly one number from list</h2>
                        <p>Intervals: {{ interval3 }}</p>
                        <p>Solution: <span class="solution">{{ solution3 }}</span></p>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h2>Your chosen number</h2>
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

