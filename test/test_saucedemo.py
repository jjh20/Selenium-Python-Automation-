import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def do_login(driver):
    """Helper reutilizable para login limpio."""
    driver.get("https://www.saucedemo.com/")
    
    # Desactivar notificaciones de Chrome para evitar errores
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # Esperar a que la página de productos cargue antes de continuar
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "title"))
    )

@pytest.mark.ui
def test_login_exitoso(driver):
    do_login(driver)
    titulo = driver.find_element(By.CLASS_NAME, "title").text
    assert titulo == "Products"
    print(f"\n✅ Login exitoso: {titulo}")

@pytest.mark.ui
def test_agregar_producto_y_checkout(driver):
    do_login(driver)

    # 1. Agregar al carrito
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
    ).click()

    # 2. Ir al carrito
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # 3. Checkout
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "checkout"))
    ).click()

    # 4. Llenar formulario — esperar que el campo esté listo
    fn_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "first-name"))
    )
    fn_field.send_keys("Juan")
    driver.find_element(By.ID, "last-name").send_keys("QA")
    driver.find_element(By.ID, "postal-code").send_keys("10101")

    # 5. Continuar
    driver.find_element(By.ID, "continue").click()

    # 6. Finalizar
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "finish"))
    ).click()

    # 7. Validación
    mensaje = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
    ).text
    assert mensaje == "Thank you for your order!"
    print(f"\n✅ ¡COMPRA COMPLETADA! Mensaje: {mensaje}")