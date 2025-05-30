from django.db import models

# 1. Modelo Race (Raça)
# Cada jogador deve escolher uma raça para jogar.
class Race(models.Model):
    # 'name' - um campo de caractere único com comprimento máximo de 255.
    name = models.CharField(max_length=255, unique=True)
    # 'description' - um campo de texto, pode ser em branco.
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Raça"
        verbose_name_plural = "Raças"

    def __str__(self):
        return self.name

# 2. Modelo Skill (Habilidade)
# Cada raça tem habilidades únicas.
class Skill(models.Model):
    # 'name' - um campo de caractere único com comprimento máximo de 255.
    name = models.CharField(max_length=255, unique=True)
    # 'bonus' - um campo de caractere com comprimento máximo de 255.
    # Descreve o tipo de bônus que os jogadores podem obter.
    bonus = models.CharField(max_length=255)
    # 'race' - uma chave estrangeira que aponta para o modelo Race.
    # A habilidade deve ser deletada quando a raça for deletada (CASCADE).
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='skills')

    class Meta:
        verbose_name = "Habilidade"
        verbose_name_plural = "Habilidades"

    def __str__(self):
        return f"{self.name} ({self.race.name})"

# 3. Modelo Guild (Guilda)
# O jogador tem a oportunidade de se tornar um membro de uma guilda.
class Guild(models.Model):
    # 'name' - um campo de caractere único com comprimento máximo de 255.
    name = models.CharField(max_length=255, unique=True)
    # 'description' - um campo de texto, pode ser nulo.
    description = models.TextField(blank=True, null=True) # blank=True para formulários, null=True para o banco de dados

    class Meta:
        verbose_name = "Guilda"
        verbose_name_plural = "Guildas"

    def __str__(self):
        return self.name

# 4. Modelo Player (Jogador)
class Player(models.Model):
    # 'nickname' - um campo de caractere único com comprimento máximo de 255.
    nickname = models.CharField(max_length=255, unique=True)
    # 'email' - um campo de e-mail com comprimento máximo de 255. Pode ser não único.
    email = models.EmailField(max_length=255)
    # 'bio' - um CharField com comprimento máximo de 255 caracteres.
    # Armazena uma breve descrição fornecida pelo usuário sobre si mesmo.
    bio = models.CharField(max_length=255)
    # 'race' - uma chave estrangeira que aponta para o modelo Race.
    # O jogador deve ser deletado quando a raça for deletada (CASCADE).
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='players')
    # 'guild' - uma chave estrangeira que aponta para o modelo Guild.
    # O jogador NÃO deve ser deletado quando a guilda for deletada (SET_NULL).
    # O campo pode ser nulo no banco de dados.
    guild = models.ForeignKey(Guild, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    # 'created_at' - um campo DateTime, que é definido com a hora atual por padrão.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Jogador"
        verbose_name_plural = "Jogadores"
        ordering = ['-created_at'] # Ordena os jogadores pelo mais recente

    def __str__(self):
        return self.nickname

