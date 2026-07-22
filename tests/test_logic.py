"""
Pruebas UNITARIAS de la lógica pura de negocio.

Estas funciones no dependen de Flask, ni de red, ni de Azure: entra un número,
sale un número. Por eso son las pruebas más rápidas y las que más casos cubren.
"""
import pytest
from app import calcular_imc, calcular_tmb, allowed_file


# ── calcular_imc ────────────────────────────────────────────────────────────
class TestCalcularImc:
    def test_peso_normal(self):
        imc, categoria = calcular_imc(70, 1.75)
        assert imc == 22.86
        assert categoria == "Peso normal"

    def test_bajo_peso(self):
        imc, categoria = calcular_imc(50, 1.75)
        assert categoria == "Bajo peso"

    def test_sobrepeso(self):
        imc, categoria = calcular_imc(80, 1.75)
        assert categoria == "Sobrepeso"

    def test_obesidad(self):
        imc, categoria = calcular_imc(100, 1.75)
        assert categoria == "Obesidad"

    # Casos LÍMITE: usamos altura=1.0 m para que el IMC sea igual al peso y
    # así probar exactamente las fronteras entre categorías (18.5, 25, 30).
    @pytest.mark.parametrize("peso, categoria_esperada", [
        (18.4, "Bajo peso"),
        (18.5, "Peso normal"),   # el límite 18.5 ya NO es bajo peso
        (24.9, "Peso normal"),
        (25.0, "Sobrepeso"),     # el límite 25 ya es sobrepeso
        (29.9, "Sobrepeso"),
        (30.0, "Obesidad"),      # el límite 30 ya es obesidad
    ])
    def test_fronteras_de_categoria(self, peso, categoria_esperada):
        _, categoria = calcular_imc(peso, 1.0)
        assert categoria == categoria_esperada

    def test_redondeo_a_dos_decimales(self):
        imc, _ = calcular_imc(70, 1.75)
        # 70 / 3.0625 = 22.857... -> debe redondear a 22.86
        assert imc == 22.86


# ── calcular_tmb ────────────────────────────────────────────────────────────
class TestCalcularTmb:
    def test_masculino_moderado(self):
        # tmb = 10*70 + 6.25*175 - 5*25 + 5 = 1673.75
        # calorias = 1673.75 * 1.55 (moderado) = 2594.31
        calorias, tmb = calcular_tmb(70, 175, 25, "masculino", "moderado")
        assert tmb == 1673.75
        assert calorias == 2594.31

    def test_femenino_usa_constante_distinta(self):
        # femenino resta 161 en vez de sumar 5 -> TMB menor que masculino
        _, tmb_f = calcular_tmb(70, 175, 25, "femenino", "moderado")
        _, tmb_m = calcular_tmb(70, 175, 25, "masculino", "moderado")
        assert tmb_f < tmb_m
        assert tmb_f == 1507.75

    @pytest.mark.parametrize("actividad, factor", [
        ("sedentario", 1.2),
        ("ligero", 1.375),
        ("moderado", 1.55),
        ("activo", 1.725),
        ("muy_activo", 1.9),
    ])
    def test_factores_de_actividad(self, actividad, factor):
        calorias, tmb = calcular_tmb(70, 175, 25, "masculino", actividad)
        assert calorias == round(tmb * factor, 2)

    def test_actividad_desconocida_usa_factor_por_defecto(self):
        # Una actividad no reconocida debe caer al factor 1.2 (sedentario).
        calorias, tmb = calcular_tmb(70, 175, 25, "masculino", "actividad_inventada")
        assert calorias == round(tmb * 1.2, 2)


# ── allowed_file ────────────────────────────────────────────────────────────
class TestAllowedFile:
    @pytest.mark.parametrize("nombre", [
        "foto.png", "imagen.jpg", "img.jpeg", "animacion.gif", "moderno.webp",
        "MAYUS.PNG",  # la extensión se compara en minúsculas
    ])
    def test_extensiones_permitidas(self, nombre):
        assert allowed_file(nombre) is True

    @pytest.mark.parametrize("nombre", [
        "documento.txt", "script.exe", "sinextension", "archivo.pdf", "",
    ])
    def test_extensiones_rechazadas(self, nombre):
        assert allowed_file(nombre) is False
