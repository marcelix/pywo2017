
class Point():
    
    # class varijabla (statička)
    dim = 2
    
    # konstruktor
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.__privatna_metoda__()
    
    # reprezentacija
    def __repr__(self):
        return "Točka (" + str(self.x) + ", " + str(self.y) + ")"
    
    # translacija
    def translate(self, vektor):
        return self >> vektor
    
    def __rshift__(self, vektor):
        return Point(self.x + vektor.x, self.y + vektor.y)
    
    # privatna metoda
    def __privatna_metoda__(self):
        pass
    
    # statička metoda
    @staticmethod
    def staticka_metoda():
        print("Pozvana statička metoda")
        
    # dekorator - isto kao i @staticmethod  
    # staticka_metoda = staticmethod(staticka_metoda)
    
class Vektor(Point):
    
    # zbrajanje
    def __add__(self, other):
        return Vektor(self.x + other.x, self.y + other.y)
            
    # skalarni produkt    
    def __mul__(self, other):
        return self.x * other.x + self.y * other.y
    
    # representation
    def __repr__(self):
        return "Vektor ({0}, {1})".format(self.x, self.y)
    
    # desno množenje
    def __rmul__(self, skalar):
        return Vektor(self.x * skalar, self.y * skalar)
    
    # HTML reprezentacija
    def _repr_html_(self):
        return "$({0}, {1})$".format(self.x, self.y)