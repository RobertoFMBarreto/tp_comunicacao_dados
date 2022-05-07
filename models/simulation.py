
class Simulation:
  def __init__(self, maquinas,trabalhos,operacoes, numero) -> None:
      self.id = numero;
      self.maquinas = maquinas;
      self.trabalhos = trabalhos;
      self.operacoes = operacoes;

  def toJson(self) -> dict:
    return{
      'id': self.id,
      'maquinas': self.maquinas,
      'trabalhos': self.trabalhos,
      'operacoes': self.operacoes
    }