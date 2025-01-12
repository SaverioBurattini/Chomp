from ezgraphics import GraphicsWindow, GraphicsImage
from random import randint
from time import sleep


def elimina_elementi_matrice(m, x, y):
  """
  La funzione accetta come parametri una matrice e di essa una colonna (x) e una riga (y).
  La matrice viene modificata in modo tale che i suoi elementi assumano valore 0 nel caso in cui il quadratino corrispondente e quelli a esso sottostanti siano stati mangiati (il quadratino rimane 1 se non è stato mangiato).
  """
  for i in range(y, len(m)):
      for j in range(x, len(m[i])):
          m[i][j] = 0



def controlla_validita_mossa(barretta, x, y):
  """
  La funzione accetta come parametri la matrice di riferimento e di essa una colonna (x) e una riga (y).
  Viene controllato se nella matrice sono presenti elementi di valore 0 nella posizione data nelle coordinate x, y.
  """
  return True if barretta[y][x] == 1 else False


def scegli_mossa_bot():
  """
  Sceglie una mossa del Computer in base alla grandezza della barretta.
  """
  x_CPU = randint(0,SIZEX-1)
  y_CPU = randint(0,SIZEY-1)
  return x_CPU, y_CPU

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
   
def aggiorna_canvas_fine_turno(canvas, barretta, cioccolato):
  canvas.clear()
  disegna_caption(canvas)
  disegna_barretta(canvas, barretta, cioccolato) # aggiorna graficamente la barretta con lo stato dei quadratini di cioccolato tenendo conto di quelli mangiati

def fine_turno(canvas, barretta, cioccolato):
  global giocatore
  giocatore = 2 if giocatore == 1 else 1
  aggiorna_canvas_fine_turno(canvas, barretta, cioccolato)


def apri_schermata_iniziale(win, canvas, cioccolato):
  canvas.clear()

  for i in range(1,3):
    canvas.drawLine((canvas.width()//3*i),0,
                    (canvas.width()//3*i),canvas.height()) # disegna sulla canvas tre linee verticali che dividono la schermata in tre sezioni utili all'utente a scegliere la modalità di gioco
    
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
  else:
      print("Errore")
      win.close()

SIZEX = 10 # grandezza griglia barretta orizzontale
SIZEY = 5 # grandezza griglia barretta verticale
CAPTION_HEIGHT = SIZEY*7.5 # grandezza della griglia della caption (solo orizzontale, prende tutto lo schermo)

def matrice_costante(nrow, ncol, v):
  """
  Restituisce una matrice di nrow righe, ncol colonne, piena di v.    
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
              canvas.drawImage(j * img.width(), i * img.height()+CAPTION_HEIGHT, img)
          if (i,j) == (0,0): # disegna un quadrato verde sul quadratino avvelenato
            canvas.setFill("green")
            canvas.drawRectangle(img.width()//4,CAPTION_HEIGHT*1.35,img.width()*0.50,img.height()*0.50)
          #227 Mr. B's contribution

def inizializza_gioco(win, canvas, cioccolato):
  global giocatore
  global modalita_di_gioco

  barretta = matrice_costante(SIZEY, SIZEX, 1) # crea una matrice di interi della dimensione della barretta che contiene 0 se un pezzetto è mangiato, 1 se non è stato ancora mangiato.

  canvas.clear()
  disegna_caption(canvas)
  disegna_barretta(canvas, barretta, cioccolato) # disegna graficamente la barretta di cioccolato per la prima volta

  def gioca_mossa(x,y):
    """
    x,y sono le coordinate della mossa da giocare.
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
    if modalita_di_gioco == 0:
      x,y = win.getMouse() # accetta l'input (click del mouse) e rimane in attesa fino a che l'utente fa una mossa valida
      gioca_mossa(x,y)

    # -------------------- Modalità Giocatore contro Computer -------------------- #
    if modalita_di_gioco == 1 and giocatore == 1: # turno del Giocatore
      x,y = win.getMouse() # accetta l'input (click del mouse) e rimane in attesa fino a che l'utente fa una mossa valida
      gioca_mossa(x,y)
    elif modalita_di_gioco == 1 and giocatore == 2: # turno del Computer
      sleep(1) # tempo di attesa in secondi prima di fare una mossa
      while True:
        x_CPU, y_CPU = scegli_mossa_bot()
        if controlla_validita_mossa(barretta, x_CPU, y_CPU):
          gioca_mossa(x_CPU, y_CPU)
          break
        else:
          pass
      
    # --------------------- Modalità Computer contro Computer -------------------- #
    if modalita_di_gioco == 2: # il turno è sempre del Computer, alternandosi fra un bot e l'altro
      sleep(1) # tempo di attesa in secondi prima di fare una mossa
      while True:
        x_CPU, y_CPU = scegli_mossa_bot()
        if controlla_validita_mossa(barretta, x_CPU, y_CPU):
          gioca_mossa(x_CPU, y_CPU)
          break
        else:
          pass

    # ---------------------- Verifica condizioni di vittoria --------------------- #
    # ------- (aprendo eventualmente la schermata di conclusione del gioco) ------ #
    if barretta[0][0] == 0: # controlla se il quadratino avvelenato è stato mangiato; se sì, apre la schermata di conclusione del gioco
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


      giocatore = 1
      win.getMouse()
      apri_schermata_iniziale(win, canvas, cioccolato)
    # ------------------------------------- - ------------------------------------ #




giocatore = 1 # variabile di stato di gioco del giocatore al valore iniziale (può assumere 1 o 2 in base al turno di quale giocatore gioca)
modalita_di_gioco = 0 # variabile che cambia in base alla modalità del gioco scelta dal giocatore (0 = PvP, 1 = PvC, 2 = CvC)
def main():
  cioccolato = GraphicsImage("chocolate.png")
  win = GraphicsWindow(SIZEX * cioccolato.width(), 
                      SIZEY * cioccolato.height() + CAPTION_HEIGHT) # crea la finestra grafica con grandezze ricavate dalla grandezza in px dell'immagine del quadratino di cioccolato
  win.setTitle("Chomp")
  canvas = win.canvas()

  apri_schermata_iniziale(win, canvas, cioccolato)

main()