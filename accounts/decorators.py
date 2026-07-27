from django.contrib.auth.decorators import login_required, user_passes_test


def es_administrador(user):
    return user.is_authenticated and user.groups.filter(name="Administrador").exists()


def es_almacenista(user):
    return user.is_authenticated and user.groups.filter(name="Almacenista").exists()


def es_gerencia(user):
    return user.is_authenticated and user.groups.filter(name="Gerencia").exists()


def es_consulta(user):
    return user.is_authenticated and user.groups.filter(name="Consulta").exists()


def admin_required(view):
    return login_required(user_passes_test(es_administrador)(view))


def almacen_required(view):
    return login_required(
        user_passes_test(
            lambda u: es_administrador(u) or es_almacenista(u)
        )(view)
    )


def gerencia_required(view):
    return login_required(
        user_passes_test(
            lambda u: es_administrador(u) or es_gerencia(u)
        )(view)
    )


def consulta_required(view):
    return login_required(
        user_passes_test(
            lambda u:
                es_administrador(u)
                or es_almacenista(u)
                or es_gerencia(u)
                or es_consulta(u)
        )(view)
    )