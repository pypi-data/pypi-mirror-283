"""
Esta es la documentacion de player
"""


class Player():
    """
    Esta clase crea un reproductor de musica
    """

    def play(self, song):
        """
        Reproduce la cancion que recibe como parametro

        Parameters:
        song (str): este es un string con el path de la cancion


        Returns:
        int: devuelve 1 si la cancion se reproduce con exito, en caso de fracaso da cero.

        """
        print("Reproduciendo cancion")

    def stop(self):
        print("Stopping")
