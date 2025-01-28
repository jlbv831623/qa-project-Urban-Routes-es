
import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import main
import time

class TestUrbanRoutes:
    driver = None
    home = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.home = main.UrbanRoutesPage(cls.driver)   #AQUI

    def test_set_route(self):                              #PASSED
        self.driver.get(data.urban_routes_url)
        routes_page = main.UrbanRoutesPage(self.driver) #AQUI

    # 1.Configurar la dirección
        address_from = data.address_from
        address_to = data.address_to
        self.driver.implicitly_wait(10)
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    # 2.Seleccionar taxi y tarifa
    def test_select_rate(self):
        self.home.select_taxi()
        self.home.select_comfort_rate()

        # Verificar que la tarifa de confort se haya seleccionado correctamente
        comfort_rate_button = self.driver.find_element(*self.home.button_comfort_xpath)
        assert 'tcard active' in comfort_rate_button.get_attribute('class'), "La tarifa comfort no fue seleccionada"

    # 3.Rellenar el número de teléfono y obtener código
    def test_get_tel_code(self):
         self.home.set_phone()
         self.home.click_on_next_button()
         self.home.code_number()
         self.home.send_cell_info()

         # Verificar que el teléfono ingresado es el esperado
         phone_number = self.home.get_phone()
         assert phone_number == data.phone_number,f"Número esperado {data.phone_number}, pero se tiene {phone_number}"

    # 4.Agregar una tarjeta de crédito
    def test_add_creditcard(self):
         self.home.card_register()
         self.home.add_card()
         self.home.close_modal()

         # Verificar que el número de tarjeta ingresado es el esperado
         card_number = self.home.get_card_input()
         assert card_number == data.card_number, f"credit card esperada {data.card_number}, pero se tiene {card_number}"

         # Verificar que el código CVV ingresado es el esperado
         cvv_code = self.home.get_cvv_card()
         assert cvv_code == data.card_code, f"CVV code esperado {data.card_code}, pero se tiene {cvv_code}"

    # 5.Escribir un mensaje para el controlador
    def test_send_message(self):
         message = data.message_for_driver
         self.home.set_message(message)

         # Verificar que el mensaje se haya ingresado correctamente
         entered_message = self.home.get_message()
         assert entered_message == message, f"Mensaje esperado {message}, pero se tiene {entered_message}"

    # 6.Pedir una manta y pañuelos
    def test_add_blanket_and_tissues(self):
        self.home.select_blanket_and_tissues()
        self.home.get_slider_status()

        # Verificar que la opción de manta y pañuelos se ha seleccionado
        assert self.home.get_slider_status() == True

    # 7.Pedir 2 helados
    def test_add_two_icecream(self):
        self.home.select_ice_cream()

        # Verificar que se han seleccionado dos helados
        assert self.home.get_icecream_counter() == '2'

    # 8.Aparece el modal para buscar un taxi
    def test_order_modal(self):
        self.home.select_order()
        order_header_title = self.home.get_order_header_title()
        assert 'Buscar automóvil' in order_header_title


    # 9.Esperar a que aparezca la información del conductor en el modal
    def test_driver_modal(self):
        # Esperar a que el modal se actualice
        time.sleep(40)

        # Verificar que el modal actualiza con el conductor visible
        order_header_title = self.home.get_driver_modal_info()
        assert 'El conductor llegará' in order_header_title, f"Se esperaba 'El conductor llegará', pero se tiene: {order_header_title}"


    @classmethod
    def teardown_class(cls):
         cls.driver.quit()



#self.driver.implicitly_wait(30)