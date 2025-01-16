import flet as ft
from converter import Conversor

def main(page: ft.Page):

    conversor = Conversor()
    list_Server, username = conversor.load_login_server_information()

    def on_change(e: ft.ControlEvent):
        if not e.control.value.isdigit():
            e.control.value = ''.join(filter(str.isdigit, e.control.value))
            e.control.update()
    
    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def add_server_to_dropdown(e):

        def add_server(e):
            server_add_value = text_field.value
            response = conversor.add_server(server_add_value)
            internal_dialog = ft.AlertDialog(
                title=ft.Text("Add Server"),
                content=ft.Text(response),
                actions=[ft.TextButton("Ok", on_click=lambda e: (close_dialog(internal_dialog), close_dialog(dialog)))]
            )
            internal_dialog.open = True
            page.overlay.append(internal_dialog)
            page.update()

            # Refresh the dropdown list
            list_Server, _ = conversor.load_login_server_information()
            server_dropdown.options = [ft.dropdown.Option(server) for server in list_Server]
            server_dropdown.update()

            close_dialog(dialog)

        text_field = ft.TextField(label="Server", hint_text="Nome do servidor", content_padding=ft.Padding(left=10, right=0, top=1, bottom=1), width=450, height=50)
        dialog = ft.AlertDialog(
                title=ft.Text("Add Server"),
                content=text_field,
                actions=[ft.TextButton("Adicionar Servidor", on_click=add_server)]
            )
        dialog.open = True
        page.overlay.append(dialog)
        page.update()

    def on_submit(e):
        # Pega os valores dos campos de texto e checkboxes
        server_value = server_dropdown.value
        database_value = database.value
        user_value = user.value
        pswd_value = pswd.value
        prefix_value = prefix.value
        add_zeros_on_left_value = add_zeros_on_left_checkbox.value
        coluna_value = coluna.value
        qtd_zeros_value = qtd_zeros.value
        use_local_database_value = use_local_database_checkbox.value

        try:
            resultado = conversor.converter(server=server_value, database=database_value, username=user_value, password=pswd_value, prefix=prefix_value, enable_Leading_Zero_Padding=add_zeros_on_left_value, padding_Columns=coluna_value, padding_Zero_Count=qtd_zeros_value, is_Local_Database=use_local_database_value)
            dialog = ft.AlertDialog(
                title=ft.Text("Sucesso"),
                content=ft.Text(resultado),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(dialog))]
            )
            
        except ValueError as errorMessage:
            dialog = ft.AlertDialog(
                title=ft.Text("Erro"),
                content=ft.Text(str(errorMessage)),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(dialog))]
            )

        dialog.open = True
        page.overlay.append(dialog)
        page.update()
    
    def switch_theme(e):
        current_theme = page.theme_mode
        if current_theme == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            convert_button.color = ft.Colors.LIGHT_BLUE_400
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            convert_button.color = ft.Colors.BLACK87

        floating_theme_button.bgcolor = theme_colors[page.theme_mode]
        floating_theme_button.icon = theme_icons[page.theme_mode]
        floating_theme_button.tooltip = f"Alterar tema. Atual: {str(page.theme_mode.name).capitalize()}"

        page.update()

    page.title = "Conversor Xlsx to SQL"
    page.window.icon = "ExceltoSQL.ico"
    page.window.width = 555
    page.window.height = 740
    page.window.maximizable = False
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK  # Começa com o tema do sistema
    page.theme = ft.Theme()  # Tema Light
    page.dark_theme = ft.Theme()

    theme_icons = {
        ft.ThemeMode.LIGHT: ft.Icons.LIGHT_MODE_SHARP,  # Ícone de sol para o tema claro
        ft.ThemeMode.DARK: ft.Icons.DARK_MODE_SHARP  # Ícone de sistema
    }

    theme_colors = {
        ft.ThemeMode.LIGHT: ft.Colors.LIGHT_BLUE_400,
        ft.ThemeMode.DARK: ft.Colors.DEEP_PURPLE_900
    }

    title = ft.Text("Conversor de Excel para SQLServer", size=18)

    list_Server_Ft = [ft.dropdown.Option(server) for server in list_Server] if list_Server != [] else []

    server_dropdown = ft.Dropdown(label="Server",options=list_Server_Ft,width=450,height=50)
    server = ft.Container(content=ft.Row(controls=[server_dropdown,ft.IconButton(icon=ft.Icons.ADD_BOX_ROUNDED,icon_color="lightblue400",icon_size=20,tooltip="Clique para adicionar um servidor", on_click=add_server_to_dropdown)]))

    database = ft.TextField(label="Database", hint_text="Nome do banco de dados", content_padding=ft.Padding(left=10, right=0, top=1, bottom=1), width=500, height=50)
    user = ft.TextField(label="Username", hint_text="Nome do usuário banco de dados", width=500, height=50)
    user.value = username
    pswd = ft.TextField(label="Password", hint_text="Senha do usuário banco de dados", password=True, width=500, height=50)
    prefix = ft.TextField(label="Prefix", hint_text="Prefixo do nome da tabela", width=500, height=50)
    add_zeros_on_left_checkbox = ft.Checkbox(label="Adicionar zeros a esquerda?", value=False, width=500, height=50, tooltip="Deixe desmarcado para não adicionar zeros a esquerda")
    coluna = ft.TextField(label="Column", hint_text="Digite as Colunas", width=500, height=50)
    qtd_zeros = ft.TextField(label="Zero Quantity", hint_text="Digite a quantidade de zeros", width=500, height=50,keyboard_type=ft.KeyboardType.NUMBER,on_change=on_change)
    use_local_database_checkbox = ft.Checkbox(label="Utilizar Banco de dados Local", value=False, width=500, height=50, tooltip="Deixe desmarcado para utilizar o banco de dados do servidor")
    convert_button = ft.Button(text='Converter',width=440, height=50, color="lightblue400",on_click=on_submit)
    divider = ft.Divider()
    padding_textfields = ft.Padding(left=10, right=10, top=0, bottom=0)
    padding_symmetric = ft.padding.symmetric(vertical=0, horizontal=10)
    
    floating_theme_button = ft.FloatingActionButton(
        icon=theme_icons[page.theme_mode],  # Ícone inicial
        on_click=switch_theme,
        bgcolor=theme_colors[page.theme_mode],  # Cor inicial
        height=50,
        width=50,
        tooltip=f"Alterar tema. Atual: {str(page.theme_mode.name).capitalize()}"
    )

    submit_theme_container = ft.Container(content=ft.Row(controls=[convert_button, floating_theme_button]))

    page.add(
            ft.Container(title, alignment=ft.alignment.center),
            ft.Container(server, alignment=ft.alignment.center_left, padding = padding_textfields),
            ft.Container(database, alignment=ft.alignment.center_left, padding = padding_textfields),
            ft.Container(user, alignment=ft.alignment.center_left, padding = padding_textfields),
            ft.Container(pswd, alignment=ft.alignment.center_left, padding = padding_textfields),
            ft.Container(prefix, alignment=ft.alignment.center_left, padding = padding_textfields),
            ft.Container(divider,padding = padding_symmetric),
            ft.Container(add_zeros_on_left_checkbox, alignment=ft.alignment.center_left, padding = padding_textfields),
            ft.Container(coluna, alignment=ft.alignment.center_left, padding = padding_textfields),
            ft.Container(qtd_zeros, alignment=ft.alignment.center_left, padding = padding_textfields),
            ft.Container(divider,padding = padding_symmetric),
            ft.Container(use_local_database_checkbox, alignment=ft.alignment.center_left, padding = padding_textfields),
            ft.Container(submit_theme_container, alignment=ft.alignment.center, padding = padding_symmetric)
        )
    
ft.app(main)