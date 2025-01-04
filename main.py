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
def aggiorna_turno_giocatore():
  # TODO scrivere sotto forma di shorthand if-else
  # giocatore = 1 if giocatore == 2 else giocatore = 1
  global giocatore
  if giocatore == 1:
    giocatore = 2
  else:
    giocatore = 1
  # TODO non print, su interfaccia grafica
  print(f"è il turno del giocatore {giocatore}")


def schermata_iniziale():
    cioccolato = GraphicsImage("chocolate.png")
    win = GraphicsWindow(SIZEX * cioccolato.width(), 
                          SIZEY * cioccolato.height()) # crea la finestra grafica con grandezze ricavate dalla grandezza in px dell'immagine del quadratino di cioccolato
    win.setTitle("Chomp")
    canvas = win.canvas()
    canvas.draw()
    win.wait()
   


SIZEX = 10
SIZEY = 5

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
            if barretta[i][j] == 1:  # Disegna solo i quadrati non mangiati
                canvas.drawImage(j * img.width(), i * img.height(), img)
            if (i,j) == (0,0):
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


giocatore = 1
def main():
    # ---------------------- Inizializzazione stato di gioco --------------------- #
    # - creare le variabili che rappresentano lo stato del gioco e impostarle al valore iniziale

    # - creare la matrice iniziale di gioco
    barretta = matrice_costante(SIZEY, SIZEX, 1)


    # ------------------------------- Parte grafica ------------------------------ #
    cioccolato = GraphicsImage("chocolate.png")
    win = GraphicsWindow(SIZEX * cioccolato.width(), 
                         SIZEY * cioccolato.height()) # crea la finestra grafica con grandezze ricavate dalla grandezza in px dell'immagine del quadratino di cioccolato
    win.setTitle("Chomp")
    canvas = win.canvas()

    disegna_barretta(canvas, barretta, cioccolato) # disegna graficamente la barretta di cioccolato per la prima volta


    while True:
      x,y = win.getMouse() # accetta l'input (click del mouse) e rimane in attesa fino a che l'utente fa una mossa valida

      colonna_matrice = x // cioccolato.width()
      riga_matrice = y // cioccolato.height()

      for i in range(riga_matrice, len(barretta)):
         for j in range(colonna_matrice, len(barretta[i])):
              barretta[i][j] = 0
      
      canvas.clear()
      disegna_barretta(canvas, barretta, cioccolato) # aggiorna graficamente la barretta con lo stato dei quadratini di cioccolato tenendo conto di quelli che ho mangiato
      print_matrix_with_indices(barretta) ## DEBUG

      aggiorna_turno_giocatore()

      # ---------------------- Verifica condizioni di vittoria --------------------- #
      if barretta[0][0] == 0: # controlla se il quadratino avvelenato è stato mangiato; se sì, esce dal ciclo
        print(f"{giocatore} vince!") # visualizza messaggio con vincitore
        canvas.clear()
        schermata_iniziale() # fine gioco

      pass

    

schermata_iniziale()