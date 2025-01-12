from ezgraphics import GraphicsWindow, GraphicsImage
from random import randint
from time import sleep


# ------------------------- Funzioni gestione matrici ------------------------ #
def matrice_costante(nrow, ncol, v):
  """
  Restituisce una matrice di nrow righe, ncol colonne, piena di v.    
  """
  m = []
  for _ in range(nrow):
      m.append([v] * ncol)
  return m


def elimina_elementi_matrice(m, x, y):
  """
  La funzione accetta come parametri una matrice e di essa una colonna (x) e una riga (y).
  La matrice viene modificata in modo tale che i suoi elementi assumano valore 0 nel caso in cui il quadratino corrispondente e quelli a esso sottostanti siano stati mangiati (il quadratino rimane 1 se non è stato mangiato).
  """
  for i in range(y, len(m)):
      for j in range(x, len(m[i])):
          m[i][j] = 0
# ------------------------ /Funzioni gestione matrici ------------------------ #





# ----------------------------- Funzioni grafiche ---------------------------- #
def apri_menu_iniziale(win, canvas, cioccolato): 
  canvas.clear()

  for i in range(1,3):
    canvas.drawLine((canvas.width()//3*i),0,
                    (canvas.width()//3*i),canvas.height()) # disegna sulla canvas due linee verticali che dividono la schermata in tre sezioni utili all'utente a scegliere la modalità di gioco
    
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
    modalita_di_gioco = 0 # Giocatore contro Giocatore
    inizializza_gioco(win, canvas, cioccolato)
  elif canvas.width()//3*1 <= x <= canvas.width()//3*2:
      modalita_di_gioco = 1 # Giocatore contro Computer
      inizializza_gioco(win, canvas, cioccolato)
  elif canvas.width()//3*2 <= x <= canvas.width()//3*3:
      modalita_di_gioco = 2 # Computer contro Computer
      inizializza_gioco(win, canvas, cioccolato)


def disegna_caption(canvas):
  canvas.setTextAnchor("center")
  canvas.setFontSize(10)
  caption = f"Turno del giocatore {giocatore}" # modalità Giocatore contro Giocatore
  if modalita_di_gioco == 2:
    caption = f"Turno del computer {giocatore}"
  elif(modalita_di_gioco == 1 and giocatore == 1): # modalità Giocatore contro Computer, turno del Giocatore
    caption = f"Turno del giocatore"
  elif(modalita_di_gioco == 1 and giocatore == 2): # modalità Giocatore contro Computer, turno del Computer
    caption = f"Turno del computer"
  canvas.drawText(canvas.width()//2, CAPTION_HEIGHT//2, f"{caption}")


def disegna_barretta(canvas, barretta, img):
  """
  Disegna la barretta di cioccolato sulla canvas.
  """
  for i in range(len(barretta)):
      for j in range(len(barretta[i])):
          if barretta[i][j] == 1:  # disegna solo i quadratini non mangiati
              canvas.drawImage(j * img.width(), i * img.height()+CAPTION_HEIGHT, img)
          if (i,j) == (0,0): # disegna un quadrato verde sul quadratino di cioccolato avvelenato
            canvas.setFill("green")
            canvas.drawRectangle(img.width()*0.25,CAPTION_HEIGHT+img.height()*0.25,img.width()*0.50,img.height()*0.50)


def disegna_canvas_gioco(canvas, barretta, cioccolato):
  """
  Resetta graficamente la canvas disegnando la caption e la barretta.
  """
  canvas.clear()
  disegna_caption(canvas)
  disegna_barretta(canvas, barretta, cioccolato) # aggiorna graficamente la barretta tenendo conto di quelli mangiati


def apri_schermata_conclusione(canvas):
      canvas.clear()
      canvas.setTextAnchor("center")
      canvas.setFontSize(25)

      testo_vincitore = f"Giocatore {giocatore} vince!"
      if modalita_di_gioco == 2:
        testo_vincitore = f"Computer {giocatore} vince!"
      elif modalita_di_gioco == 1 and giocatore == 1:
        testo_vincitore = f"Giocatore vince!"
      elif modalita_di_gioco == 1 and giocatore == 2:
        testo_vincitore = f"Computer vince!"
      canvas.drawText(canvas.width()//2, canvas.height()//2, f"{testo_vincitore}") # visualizza sulla canvas il testo con l'annuncio del vincitore
      canvas.setFontSize(10)
      canvas.drawText(canvas.width()//2,canvas.height()//2+30,f"Clicca sullo schermo per tornare alla schermata iniziale")
# ---------------------------- /Funzioni grafiche ---------------------------- #




# ----------------------------- Funzioni di gioco ---------------------------- #
def scegli_mossa_bot():
  """
  Sceglie una mossa del Computer in base alla grandezza della barretta.
  """
  x_CPU = randint(0,SIZEX-1)
  y_CPU = randint(0,SIZEY-1)
  return x_CPU, y_CPU


def controlla_validita_mossa(barretta, x, y):
  """
  La funzione accetta come parametri la matrice barretta e di essa una colonna (x) e una riga (y).
  Viene controllato se nella matrice sono presenti elementi di valore 1 nella posizione data nelle coordinate x,y.
  """
  return True if barretta[y][x] == 1 else False


def fine_turno(canvas, barretta, cioccolato):
  """
  Aggiorna la variabile giocatore e, graficamente, resetta la canvas ridisegnando la caption e la barretta.
  """
  global giocatore
  giocatore = 2 if giocatore == 1 else 1
  disegna_canvas_gioco(canvas, barretta, cioccolato)


def inizializza_gioco(win, canvas, cioccolato):
  """
  In base alla modalità di gioco scelta dal giocatore, si avvierà una sequenza di richieste di input da parte del giocatore e/o del computer, fino a che le condizioni di vittoria non saranno soddisfatte per uno dei due giocatori.
  """
  global giocatore
  global modalita_di_gioco

  barretta = matrice_costante(SIZEY, SIZEX, 1) # crea una matrice piena di 1, delle dimensioni della barretta, che contiene 0 se un quadratino è stato mangiato, 1 se non è stato ancora mangiato

  disegna_canvas_gioco(canvas, barretta, cioccolato) # disegna graficamente la caption e la barretta di cioccolato per la prima volta


  def gioca_mossa(x,y):
    """
    In base alla modalità di gioco, viene giocata la mossa per le coordinate x,y.
    """
    
    if modalita_di_gioco == 0 or (modalita_di_gioco == 1 and giocatore == 1): # se è il turno del giocatore, divide l'output di getMouse() per la grandezza dell'immagine del quadratino
      y -= CAPTION_HEIGHT # la coordinata y deve tenere in considerazione lo spazio verticale occupato dalla caption
      x = int(x // cioccolato.width())
      y = int(y // cioccolato.height())

    if 0 <= x < SIZEX and 0 <= y < SIZEY: # controlla se il click input dell'utente è avvenuto nella griglia della barretta
      if controlla_validita_mossa(barretta, x, y):
        elimina_elementi_matrice(barretta, x, y)
        fine_turno(canvas, barretta, cioccolato)


  while True:
    # -------------------- Modalità Giocatore contro Giocatore ------------------- #
    if modalita_di_gioco == 0: # il turno è sempre del Giocatore, alternandosi fra un giocatore e l'altro
      x,y = win.getMouse() # accetta l'input (click del mouse) e rimane in attesa fino a che l'utente fa una mossa valida
      gioca_mossa(x,y)


    # -------------------- Modalità Giocatore contro Computer -------------------- #
    if modalita_di_gioco == 1 and giocatore == 1: # turno del Giocatore
      x,y = win.getMouse()
      gioca_mossa(x,y)
    elif modalita_di_gioco == 1 and giocatore == 2: # turno del Computer
      sleep(1) # tempo di attesa in secondi prima che la mossa venga giocata
      while True:
        x_CPU, y_CPU = scegli_mossa_bot()
        if controlla_validita_mossa(barretta, x_CPU, y_CPU):
          gioca_mossa(x_CPU, y_CPU)
          break

      
    # --------------------- Modalità Computer contro Computer -------------------- #
    if modalita_di_gioco == 2: # il turno è sempre del Computer, alternandosi fra un bot e l'altro
      sleep(1)
      while True:
        x_CPU, y_CPU = scegli_mossa_bot()
        if controlla_validita_mossa(barretta, x_CPU, y_CPU):
          gioca_mossa(x_CPU, y_CPU)
          break


    # ---------------------- Verifica condizioni di vittoria --------------------- #
    # ------- (aprendo eventualmente la schermata di conclusione del gioco) ------ #
    if barretta[0][0] == 0: # controlla se il quadratino avvelenato è stato mangiato; se sì, apre la schermata di conclusione del gioco
      apri_schermata_conclusione(canvas)
      giocatore = 1 # viene resettata la variabile giocatore per eventuali prossime partite


      win.getMouse()
      apri_menu_iniziale(win, canvas, cioccolato)
# ---------------------------- /Funzioni di gioco ---------------------------- #





SIZEX = 10 # quantità di quadratini della barretta sull'asse delle x
SIZEY = 5 # quantità di quadratini della barretta sull'asse delle y
CAPTION_HEIGHT = SIZEY * 7.5 # altezza della caption; maggiore è la quantità di quadratini sull'asse delle y, più grande sarà la grandezza della caption


# ------------------------- Variabili stato di gioco ------------------------- #
giocatore = 1 # settata al valore iniziale di 1; può assumere valore 1 o 2 in base al turno del giocatore; alla fine del gioco viene resettata al suo valore iniziale
modalita_di_gioco = 0 # varia in base alla modalità del gioco scelta dal giocatore (0 = PvP, 1 = PvC, 2 = CvC)


def main():
  cioccolato = GraphicsImage("chocolate.png")
  win = GraphicsWindow(SIZEX * cioccolato.width(), 
                      SIZEY * cioccolato.height() + CAPTION_HEIGHT) # crea la finestra grafica con grandezze ricavate dalla grandezza in px dell'immagine del quadratino di cioccolato e l'altezza della caption
  canvas = win.canvas()
  win.setTitle("Chomp")

  apri_menu_iniziale(win, canvas, cioccolato)


main()