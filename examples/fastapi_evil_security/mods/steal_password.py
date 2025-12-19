import universal_modloader as uml


@uml.Inject("app", "create_user", at=uml.At.HEAD())
@uml.Inject("app", "update_user", at=uml.At.HEAD())
def sniff_password(ctx):
    user_in = ctx["user_in"]
    print(
        f"\033[31m[Mod]\033[0m Got Email: \033[95m{user_in.email}\033[0m, Password: \033[95m{user_in.password}\033[0m"
    )


@uml.Inject("app", "login", at=uml.At.HEAD())
def sniff_login_password(ctx):
    credentials = ctx["credentials"]
    print(
        f"\033[31m[Mod]\033[0m Login Attempt - Email: \033[95m{credentials.email}\033[0m, Password: \033[95m{credentials.password}\033[0m"
    )
