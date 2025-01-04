from ezgraphics import GraphicsWindow, GraphicsImage
"""
STATO DEL GIOCO:
   - il giocatore che deve muovere
     + un variabile intera "giocatore" che vale o 1 o 2
   - quali pezzi sono stati  mangiati e quali no
     + una matrice di interi della dimensione della barretta
       che contiene 0 se un pezzetto è mangiato, 1 se
       non è stato ancora mangiato.
"""

# ---------------------------------------------------------------------------- #
#                                Stato del gioco                               #
# ---------------------------------------------------------------------------- #

def aggiungi_caption_canvas(canvas):
  canvas.drawLine(0, canvas.height()-SIZEY_CAPTION+5, canvas.width(), canvas.height()-SIZEY_CAPTION+5)
  canvas.setTextAnchor("center")
  canvas.setFontSize(10)
  canvas.drawText(canvas.width()//2, canvas.height()-SIZEY_CAPTION//2, f"Turno giocatore {giocatore}")
   
def aggiorna_canvas_fine_turno(canvas, barretta, cioccolato):
  global giocatore
  giocatore = 2 if giocatore == 1 else 1
  canvas.clear()
  aggiungi_caption_canvas(canvas)
  disegna_barretta(canvas, barretta, cioccolato) # aggiorna graficamente la barretta con lo stato dei quadratini di cioccolato tenendo conto di quelli mangiati


def schermata_iniziale(win, canvas, cioccolato):
    canvas.clear()

    for i in range(1,3):
      canvas.drawLine((canvas.width()//3*i),0,(canvas.width()//3*i),canvas.height())
    
    x,y = win.getMouse()
    inizializza_gioco(win, canvas, cioccolato)



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

# Variabili stato di gioco ai valori iniziali
giocatore = 1
def main():
  cioccolato = GraphicsImage("chocolate.png")
  win = GraphicsWindow(SIZEX * cioccolato.width(), 
                      SIZEY * cioccolato.height() + SIZEY_CAPTION) # crea la finestra grafica con grandezze ricavate dalla grandezza in px dell'immagine del quadratino di cioccolato
  win.setTitle("Chomp")
  canvas = win.canvas()
  schermata_iniziale(win, canvas, cioccolato)  

def inizializza_gioco(win, canvas, cioccolato):
  canvas.clear()

  barretta = matrice_costante(SIZEY, SIZEX, 1) # crea la matrice iniziale di gioco



  aggiungi_caption_canvas(canvas)
  disegna_barretta(canvas, barretta, cioccolato) # disegna graficamente la barretta di cioccolato per la prima volta


  while True:
    x,y = win.getMouse() # accetta l'input (click del mouse) e rimane in attesa fino a che l'utente fa una mossa valida

    colonna_matrice = x // cioccolato.width()
    riga_matrice = y // cioccolato.height()

    for i in range(riga_matrice, len(barretta)):
        for j in range(colonna_matrice, len(barretta[i])):
            barretta[i][j] = 0
    
    aggiorna_canvas_fine_turno(canvas, barretta, cioccolato)

    print_matrix_with_indices(barretta) ## DEBUG


    # ---------------------- Verifica condizioni di vittoria --------------------- #
    if barretta[0][0] == 0: # controlla se il quadratino avvelenato è stato mangiato; se sì, apre la schermata di conclusione del gioco
      canvas.clear()
      canvas.setTextAnchor("center")
      canvas.setFontSize(25)
      canvas.drawText(canvas.width()//2,canvas.height()//2,f"Giocatore {giocatore} vince!") # visualizza sulla canvas il testo con l'annuncio del vincitore
      canvas.setFontSize(10)
      canvas.drawText(canvas.width()//2,canvas.height()//2+30,f"Clicca sullo schermo per tornare alla schermata iniziale")

      win.getMouse()
      schermata_iniziale(win, canvas, cioccolato)


main()