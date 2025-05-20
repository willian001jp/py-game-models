# main.py
import os
import django
import json

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings') # Substitua 'your_project_name' pelo nome do seu projeto Django
django.setup()

# Importa os modelos depois que o Django for configurado
# Ajuste o caminho de importação conforme a localização dos seus modelos
from your_app.models import Race, Skill, Guild, Player # Ou from db.models import Race, Skill, Guild, Player, se seus modelos estiverem em db/models.py


def main():
    """
    Lê os dados dos jogadores de 'players.json' e os adiciona ao banco de dados.
    Usa get_or_create() para evitar duplicação de raças, guildas e habilidades.
    """
    try:
        with open('players.json', 'r', encoding='utf-8') as f:
            players_data = json.load(f)
    except FileNotFoundError:
        print("Erro: O arquivo 'players.json' não foi encontrado. Certifique-se de que ele está na mesma pasta que 'main.py'.")
        return
    except json.JSONDecodeError:
        print("Erro: Não foi possível decodificar o arquivo 'players.json'. Verifique a formatação JSON.")
        return

    for player_data in players_data:
        print(f"Processando jogador: {player_data['nickname']}")

        # 1. Processar Raça
        race_info = player_data['race']
        race_obj, created = Race.objects.get_or_create(
            name=race_info['name'],
            defaults={'description': race_info.get('description', '')}
        )
        if created:
            print(f"  Raça '{race_obj.name}' criada.")
        else:
            print(f"  Raça '{race_obj.name}' já existe.")

        # 2. Processar Guilda (se existir)
        guild_obj = None
        guild_info = player_data.get('guild')
        if guild_info:
            guild_obj, created = Guild.objects.get_or_create(
                name=guild_info['name'],
                defaults={'description': guild_info.get('description', '')}
            )
            if created:
                print(f"  Guilda '{guild_obj.name}' criada.")
            else:
                print(f"  Guilda '{guild_obj.name}' já existe.")
        else:
            print("  Jogador não possui guilda.")

        # 3. Criar ou Obter o Jogador
        player_obj, created = Player.objects.get_or_create(
            nickname=player_data['nickname'],
            defaults={
                'email': player_data['email'],
                'bio': player_data['bio'],
                'race': race_obj,
                'guild': guild_obj
            }
        )
        if created:
            print(f"  Jogador '{player_obj.nickname}' criado.")
        else:
            print(f"  Jogador '{player_obj.nickname}' já existe. Atualizando dados (se necessário)...")
            # Opcional: Você pode atualizar os campos do jogador aqui se ele já existir
            # player_obj.email = player_data['email']
            # player_obj.bio = player_data['bio']
            # player_obj.race = race_obj
            # player_obj.guild = guild_obj
            # player_obj.save()

        # 4. Processar Habilidades
        skills_info = player_data.get('skills', [])
        for skill_info in skills_info:
            skill_obj, created = Skill.objects.get_or_create(
                name=skill_info['name'],
                race=race_obj, # Associa a habilidade à raça do jogador
                defaults={'bonus': skill_info['bonus']}
            )
            if created:
                print(f"    Habilidade '{skill_obj.name}' para '{race_obj.name}' criada.")
            else:
                print(f"    Habilidade '{skill_obj.name}' para '{race_obj.name}' já existe.")

    print("\nProcessamento de jogadores concluído.")

if __name__ == '__main__':
    main()