# p8xxpy/styles.py
def apply_style(widget, style):
    """
    Aplica um estilo ao widget fornecido.

    Parâmetros:
    widget (object): O widget da interface gráfica.
    style (dict): Um dicionário com as propriedades de estilo.
    """
    for key, value in style.items():
        widget[key] = value
