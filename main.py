from ezgraphics import GraphicsWindow, GraphicsImage
from random import randint


def elimina_quadratini_matrice_barretta(barretta, x, y):
  """
  La funzione accetta come parametri la matrice di riferimento e di essa una colonna (x) e una riga (y).
  La matrice viene modificata in modo tale che i suoi elementi assumano valore 0 nel caso in cui il quadratino corrispondente e quelli a sé sottostanti siano stati mangiati (il quadratino rimane 1 se non è stato mangiato).
  """
  for i in range(y, len(barretta)):
      for j in range(x, len(barretta[i])):
          barretta[i][j] = 0

def controlla_quadratini_matrice_barretta(barretta, x, y):
  """
  La funzione accetta come parametri la matrice di riferimento e di essa una colonna (x) e una riga (y).
  Viene controllato se nella matrice sono presenti elementi di valore 0 nella posizione data nelle coordinate x, y.
  """
  return True if barretta[y][x] == 1 else False


def scegli_mossa_bot():
  x_CPU = randint(1,SIZEX)
  y_CPU = randint(1,SIZEY)
  return x_CPU, y_CPU

def aggiungi_caption_canvas(canvas):
  canvas.drawLine(0, canvas.height()-SIZEY_CAPTION+5, canvas.width(), canvas.height()-SIZEY_CAPTION+5)
  canvas.setTextAnchor("center")
  canvas.setFontSize(10)
  canvas.drawText(canvas.width()//2, canvas.height()-SIZEY_CAPTION//2, f"Turno giocatore {giocatore}")
   
def aggiorna_canvas_fine_turno(canvas, barretta, cioccolato):
  canvas.clear()
  aggiungi_caption_canvas(canvas)
  disegna_barretta(canvas, barretta, cioccolato) # aggiorna graficamente la barretta con lo stato dei quadratini di cioccolato tenendo conto di quelli mangiati


def apri_schermata_iniziale(win, canvas, cioccolato):
  canvas.clear()

  for i in range(1,3):
    canvas.drawLine((canvas.width()//3*i),0,(canvas.width()//3*i),canvas.height())
    
  for i in range(1,4):
    canvas.setTextAnchor("center")
    canvas.setFontSize(9)
    if i == 1:
      canvas.drawText(canvas.width()//6,canvas.height()//2,"Giocatore contro Giocatore")
    elif i == 2:
        canvas.drawText(canvas.width()//2,canvas.height()//2,"Giocatore contro Computer")
    elif i == 3:
        canvas.drawText(canvas.width()//1.2,canvas.height()/2,"Computer contro Computer")
  
  x,y = win.getMouse()
  global modalita_di_gioco
  if 0 <= x <= canvas.width()//3*1:
    inizializza_gioco(win, canvas, cioccolato)
  elif canvas.width()//3*1 <= x <= canvas.width()//3*2:
      modalita_di_gioco = 1
  elif canvas.width()//3*2 <= x <= canvas.width()//3*3:
      modalita_di_gioco = 2
  else:
      print("Errore")
      win.close()

SIZEX = 10 # grandezza griglia barretta orizzontale
SIZEY = 5 # grandezza griglia barretta verticale
SIZEY_CAPTION = SIZEY*7.5

def matrice_costante(nrow, ncol, v):
  """
  Restituisce una matrice di nrow righe, ncol colonne,
  piena di v.    
  """
  m = []
  for _ in range(nrow):
      m.append([v] * ncol)
  return m

def disegna_barretta(canvas, barretta, img):
  """
  Disegna la barretta di cioccolato sul canvas.
  """
  for i in range(len(barretta)):
      for j in range(len(barretta[i])):
          if barretta[i][j] == 1:  # disegna solo i quadrati non mangiati
              canvas.drawImage(j * img.width(), i * img.height(), img)
          if (i,j) == (0,0): # disegna un quadrato verde sul quadratino avvelenato
            canvas.setFill("green")
            canvas.drawRectangle(0,0,img.width()*0.75,img.height()*0.75)

def print_matrix_with_indices(matrix):
    # Loop over each row
    for i in range(len(matrix)):
        # Loop over each column in the current row
        for j in range(len(matrix[i])):
            # Print element at row i, column j
            print(matrix[i][j], end=' ')
        # Print a new line after each row
        print()

giocatore = 1 # variabile di stato di gioco del giocatore al valore iniziale (può assumere 1 o 2 in base al turno di quale giocatore gioca)
modalita_di_gioco = 0 # variabile che cambia in base alla modalità del gioco scelta dal giocatore (0 = PvP, 1 = PvC, 2 = CvC)
def main():
  cioccolato = GraphicsImage("chocolate.png")
  win = GraphicsWindow(SIZEX * cioccolato.width(), 
                      SIZEY * cioccolato.height() + SIZEY_CAPTION) # crea la finestra grafica con grandezze ricavate dalla grandezza in px dell'immagine del quadratino di cioccolato
  win.setTitle("Chomp")
  canvas = win.canvas()
  apri_schermata_iniziale(win, canvas, cioccolato)  

def inizializza_gioco(win, canvas, cioccolato):
  global giocatore
  global modalita_di_gioco

  barretta = matrice_costante(SIZEY, SIZEX, 1) # crea una matrice di interi della dimensione della barretta che contiene 0 se un pezzetto è mangiato, 1 se non è stato ancora mangiato.

  canvas.clear()
  aggiungi_caption_canvas(canvas)
  disegna_barretta(canvas, barretta, cioccolato) # disegna graficamente la barretta di cioccolato per la prima volta


  while True:
    # -------------------- Modalità Giocatore contro Giocatore ------------------- #

    if modalita_di_gioco == 0:
      x,y = win.getMouse() # accetta l'input (click del mouse) e rimane in attesa fino a che l'utente fa una mossa valida
      colonna_matrice = x // cioccolato.width()
      riga_matrice = y // cioccolato.height()
      if controlla_quadratini_matrice_barretta(barretta, colonna_matrice, riga_matrice):
        elimina_quadratini_matrice_barretta(barretta, colonna_matrice, riga_matrice)
        giocatore = 2 if giocatore == 1 else 1
        aggiorna_canvas_fine_turno(canvas, barretta, cioccolato)




    # # -------------------- Modalità Giocatore contro Computer -------------------- #
    # if modalita_di_gioco == 1 and giocatore == 1:
    #   while True:
    #     x,y = win.getMouse()
    #     if x or y == 0 in barretta:
    #       x,y = win.getMouse()
    #     else:
    #       elimina_quadratini_matrice_barretta(barretta, colonna_matrice, riga_matrice)
    # if modalita_di_gioco == 1 and giocatore == 2:
    #   while True:
    #     x_CPU, y_CPU = scegli_mossa_bot()
    #     if x_CPU or y_CPU == 0 in barretta:
    #       x_CPU, y_CPU = scegli_mossa_bot()
    #     else:
    #       elimina_quadratini_matrice_barretta(barretta, x_CPU, y_CPU)



  

    # ---------------------- Verifica condizioni di vittoria --------------------- #
    # ------- (aprendo eventualmente la schermata di conclusione del gioco) ------ #
    if barretta[0][0] == 0: # controlla se il quadratino avvelenato è stato mangiato; se sì, apre la schermata di conclusione del gioco
      canvas.clear()
      canvas.setTextAnchor("center")
      canvas.setFontSize(25)
      canvas.drawText(canvas.width()//2,canvas.height()//2,f"Giocatore {giocatore} vince!") # visualizza sulla canvas il testo con l'annuncio del vincitore
      canvas.setFontSize(10)
      canvas.drawText(canvas.width()//2,canvas.height()//2+30,f"Clicca sullo schermo per tornare alla schermata iniziale")

      giocatore = 1
      win.getMouse()
      apri_schermata_iniziale(win, canvas, cioccolato)
      # ------------------------------------- - ------------------------------------ #





main()