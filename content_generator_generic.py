#!/usr/bin/env python3
"""
Générateur de contenu éditorial générique configurable
Génère des articles structurés en JSON à partir de sujets fournis pour n'importe quelle thématique
"""

import os
import sys
import json
import argparse
import configparser
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from openai import OpenAI
    from slugify import slugify
    import markdown
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Dépendance manquante: {e}")
    print("Installez avec: pip install openai python-slugify markdown python-dotenv")
    sys.exit(1)

# Charger les variables d'environnement
load_dotenv()

class ThematicContentGenerator:
    def __init__(self, config_file: str = None):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        
        if not self.api_key:
            print("❌ OPENAI_API_KEY non trouvée dans les variables d'environnement")
            print("Créez un fichier .env avec: OPENAI_API_KEY=sk-...")
            sys.exit(1)
        
        self.client = OpenAI(api_key=self.api_key)
        
        # Configuration par défaut
        self.config = {
            'site_name': 'MonSite.fr',
            'domain': 'MonSite.fr',
            'theme': 'général',
            'target_audience': 'grand public',
            'tone': 'professionnel et accessible',
            'content_type': 'article informatif',
            'internal_links_prefix': ['/blog/', '/guide/', '/conseil/'],
            'expertise_level': 'expert dans le domaine',
            'content_style': 'pédagogique et pratique',
            'exclusions': {
                'brands': [],
                'cities': [],
                'competitors': [],
                'custom': []
            }
        }
        
        # Charger la configuration depuis le fichier si fourni
        if config_file and Path(config_file).exists():
            self.load_config(config_file)
        
        # Configuration Markdown
        self.md = markdown.Markdown(
            extensions=['tables', 'fenced_code', 'sane_lists', 'toc']
        )
    
    def load_config(self, config_file: str):
        """Charge la configuration depuis un fichier INI"""
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')
        
        if 'THEME' in config:
            self.config.update(dict(config['THEME']))
        
        # Charger les exclusions si présentes
        if 'EXCLUSIONS' in config:
            exclusions_data = dict(config['EXCLUSIONS'])
            for key, value in exclusions_data.items():
                if value:
                    # Séparer les valeurs par virgule et nettoyer
                    self.config['exclusions'][key] = [item.strip() for item in value.split(',') if item.strip()]
    
    def _build_exclusions_text(self) -> str:
        """Construit le texte des exclusions pour le prompt"""
        exclusions_parts = []
        
        if self.config['exclusions']['brands']:
            brands_list = ', '.join(self.config['exclusions']['brands'])
            exclusions_parts.append(f"- INTERDIT de citer ces marques : {brands_list}")
        
        if self.config['exclusions']['cities']:
            cities_list = ', '.join(self.config['exclusions']['cities'])
            exclusions_parts.append(f"- INTERDIT de mentionner ces villes : {cities_list}")
        
        if self.config['exclusions']['competitors']:
            competitors_list = ', '.join(self.config['exclusions']['competitors'])
            exclusions_parts.append(f"- INTERDIT de mentionner ces concurrents : {competitors_list}")
        
        if self.config['exclusions']['custom']:
            custom_list = ', '.join(self.config['exclusions']['custom'])
            exclusions_parts.append(f"- INTERDIT ces mots/expressions : {custom_list}")
        
        if exclusions_parts:
            return "\n\nRESTRICTIONS ÉDITORIALES :\n" + "\n".join(exclusions_parts)
        
        return ""
    
    def generate_system_prompt(self) -> str:
        """Génère le prompt système adapté à la thématique"""
        
        # Construire les exclusions
        exclusions_text = self._build_exclusions_text()
        
        return f"""Tu es un rédacteur expert pour {self.config['site_name']} (domaine: {self.config['domain']}). 

THÉMATIQUE : {self.config['theme']}
EXPERTISE : {self.config['expertise_level']}
PUBLIC CIBLE : {self.config['target_audience']}
TON : {self.config['tone']}
TYPE DE CONTENU : {self.config['content_type']}

Contraintes éditoriales :
- Public cible : {self.config['target_audience']} ; ton {self.config['tone']}.
- Style : {self.config['content_style']}, bien structuré avec H1 titre, intro courte, sections H2/H3.
- Structure pratique : listes, conseils concrets, exemples, points clés.
- SEO : méta-titre (≤60), méta-description (≤155), slug, 5 mots-clés pertinents, FAQ 3–5 Q/R en JSON-LD (FAQPage).
- Liaisons internes : propose 3 slugs internes plausibles avec ces préfixes {self.config['internal_links_prefix']} sans URL absolue.
- Style : Markdown propre, phrases claires, pas d'emojis ni de contenu superflu.
- Interdit : jargon excessif, promesses irréalistes, contenu dupliqué.
{exclusions_text}

IMPORTANT: Tu dois répondre UNIQUEMENT avec un JSON valide dans ce format exact :
{{
  "title": "string",
  "slug": "string-kebab",
  "seo_title": "string",
  "seo_description": "string",
  "keywords": ["str","str","str","str","str"],
  "content_markdown": "markdown",
  "faq_jsonld": {{ "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [] }},
  "internal_links": ["{self.config['internal_links_prefix'][0]}...","{self.config['internal_links_prefix'][1]}...","{self.config['internal_links_prefix'][2]}..."]
}}"""

    def clean_slug(self, text: str, max_length: int = 80) -> str:
        """Crée un slug propre à partir du texte"""
        slug = slugify(text, max_length=max_length)
        # Nettoyer les doublons de tirets
        while '--' in slug:
            slug = slug.replace('--', '-')
        return slug.strip('-')
    
    def generate_content(self, topic: str, level: str) -> Optional[Dict[str, Any]]:
        """Génère le contenu pour un sujet donné"""
        user_prompt = f"""Génère un {self.config['content_type']} de niveau {level} sur le sujet : "{topic}"

CONTEXTE THÉMATIQUE : {self.config['theme']}
NIVEAU : {level}
PUBLIC : {self.config['target_audience']}

Le contenu doit être adapté au niveau {level} et suivre toutes les contraintes éditoriales mentionnées.
Assure-toi que la FAQ contient 3-5 questions/réponses pertinentes au format JSON-LD.
Les liens internes doivent être des chemins relatifs plausibles pour un site sur {self.config['theme']}.

Réponds UNIQUEMENT avec le JSON demandé, sans texte additionnel."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.generate_system_prompt()},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            content_text = response.choices[0].message.content.strip()
            
            # Nettoyer la réponse au cas où il y aurait du texte avant/après le JSON
            start_idx = content_text.find('{')
            end_idx = content_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("Aucun JSON valide trouvé dans la réponse")
            
            json_content = content_text[start_idx:end_idx]
            
            # Parser le JSON
            data = json.loads(json_content)
            
            # Valider et nettoyer le slug
            if not data.get('slug') or not isinstance(data['slug'], str):
                data['slug'] = self.clean_slug(data.get('title', topic))
            else:
                data['slug'] = self.clean_slug(data['slug'])
            
            # Générer le HTML à partir du Markdown
            if 'content_markdown' in data:
                self.md.reset()  # Reset pour éviter les conflits entre articles
                data['content_html'] = self.md.convert(data['content_markdown'])
            
            # Valider la structure minimale
            required_fields = ['title', 'slug', 'seo_title', 'seo_description', 
                             'keywords', 'content_markdown', 'faq_jsonld', 'internal_links']
            
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                raise ValueError(f"Champs manquants: {', '.join(missing_fields)}")
            
            return data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON invalide retourné par l'API: {e}")
        except Exception as e:
            raise ValueError(f"Erreur lors de la génération: {e}")
    
    def save_content(self, data: Dict[str, Any], output_dir: Path) -> str:
        """Sauvegarde le contenu dans un fichier JSON"""
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = f"{timestamp}-{data['slug']}.json"
        filepath = output_dir / filename
        
        # Créer le répertoire s'il n'existe pas
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarder avec une indentation propre
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filename

def create_default_config():
    """Crée un fichier de configuration par défaut"""
    config_content = """[THEME]
# Configuration de base
site_name = MonSite.fr
domain = monsite.fr
theme = général
target_audience = grand public
tone = professionnel et accessible
content_type = article informatif
expertise_level = expert dans le domaine
content_style = pédagogique et pratique

# Préfixes pour les liens internes (séparer par des virgules)
internal_links_prefix = ["/blog/", "/guide/", "/conseil/"]

# Exemples de configurations thématiques :
# 
# CUISINE :
# theme = cuisine et gastronomie
# target_audience = passionnés de cuisine
# tone = chaleureux et expert
# content_type = recette ou guide culinaire
# internal_links_prefix = ["/recettes/", "/techniques/", "/ingredients/"]
#
# TECH :
# theme = technologie et développement
# target_audience = développeurs et passionnés tech
# tone = technique et précis
# content_type = tutoriel technique
# internal_links_prefix = ["/tutos/", "/outils/", "/frameworks/"]
#
# SANTÉ :
# theme = santé et bien-être
# target_audience = personnes soucieuses de leur santé
# tone = bienveillant et informatif
# content_type = conseil santé
# internal_links_prefix = ["/conseils/", "/nutrition/", "/exercices/"]
"""
    
    with open('config_theme.ini', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("📝 Fichier config_theme.ini créé avec des exemples de configuration")
    print("Modifiez-le selon votre thématique et relancez le script")

def create_example_topics():
    """Crée un fichier topics.txt d'exemple générique"""
    example_topics = [
        "Guide pour débutants",
        "Techniques avancées",
        "Erreurs courantes à éviter"
    ]
    
    with open('topics.txt', 'w', encoding='utf-8') as f:
        for topic in example_topics:
            f.write(f"{topic}\n")
    
    print("📝 Fichier topics.txt créé avec des exemples génériques")
    print("Modifiez-le avec vos sujets spécifiques et relancez le script")

def main():
    parser = argparse.ArgumentParser(
        description="Générateur de contenu éditorial générique configurable"
    )
    parser.add_argument(
        '--topics', 
        nargs='*', 
        help='Liste des sujets à traiter'
    )
    parser.add_argument(
        '--level', 
        choices=['débutant', 'intermédiaire', 'avancé'],
        default='intermédiaire',
        help='Niveau de difficulté du contenu (défaut: intermédiaire)'
    )
    parser.add_argument(
        '--out', 
        default='out',
        help='Répertoire de sortie (défaut: out)'
    )
    parser.add_argument(
        '--config',
        default='config_theme.ini',
        help='Fichier de configuration thématique (défaut: config_theme.ini)'
    )
    parser.add_argument(
        '--domain',
        help='Nom de domaine du site (ex: monsite.fr)'
    )
    parser.add_argument(
        '--exclude-brands',
        help='Marques à exclure, séparées par des virgules (ex: "Nike,Adidas,Puma")'
    )
    parser.add_argument(
        '--exclude-cities',
        help='Villes à exclure, séparées par des virgules (ex: "Paris,Lyon,Marseille")'
    )
    parser.add_argument(
        '--exclude-competitors',
        help='Concurrents à exclure, séparées par des virgules'
    )
    parser.add_argument(
        '--exclude-custom',
        help='Mots/expressions personnalisés à exclure, séparés par des virgules'
    )
    parser.add_argument(
        '--theme',
        help='Thème principal pour la génération (ex: "Jardinage en hiver")'
    )
    parser.add_argument(
        '--count',
        type=int,
        default=5,
        help='Nombre d\'articles à générer (défaut: 5)'
    )
    parser.add_argument(
        '--output-html',
        action='store_true',
        help='Générer les pages HTML avec maillage interne'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Mode verbeux pour afficher plus de détails'
    )
    parser.add_argument(
        '--time',
        action='store_true',
        help='Mesurer et afficher le temps d\'exécution'
    )
    parser.add_argument(
        '--init-config',
        action='store_true',
        help='Créer un fichier de configuration par défaut'
    )
    
    args = parser.parse_args()
    
    # Créer la configuration par défaut si demandé
    if args.init_config:
        create_default_config()
        return
    
    # Vérifier si le fichier de config existe
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"❌ Fichier de configuration {args.config} introuvable")
        print("Utilisez --init-config pour créer un fichier de configuration par défaut")
        return
    
    # Déterminer les sujets à traiter
    topics = []
    
    if args.topics:
        topics = args.topics
    else:
        topics_file = Path('topics.txt')
        if not topics_file.exists():
            create_example_topics()
            return
        
        with open(topics_file, 'r', encoding='utf-8') as f:
            topics = [line.strip() for line in f if line.strip()]
    
    if not topics:
        print("❌ Aucun sujet à traiter")
        return
    
    # Initialiser le générateur avec la configuration
    generator = ThematicContentGenerator(args.config)
    
    # Appliquer les paramètres de ligne de commande
    if args.domain:
        generator.config['domain'] = args.domain
        # Mettre à jour le site_name si pas déjà personnalisé
        if generator.config['site_name'] == 'MonSite.fr':
            generator.config['site_name'] = args.domain
    
    # Appliquer le thème si fourni
    if args.theme:
        generator.config['theme'] = args.theme
    
    # Appliquer les exclusions depuis la ligne de commande
    if args.exclude_brands:
        generator.config['exclusions']['brands'] = [item.strip() for item in args.exclude_brands.split(',') if item.strip()]
    
    if args.exclude_cities:
        generator.config['exclusions']['cities'] = [item.strip() for item in args.exclude_cities.split(',') if item.strip()]
    
    if args.exclude_competitors:
        generator.config['exclusions']['competitors'] = [item.strip() for item in args.exclude_competitors.split(',') if item.strip()]
    
    if args.exclude_custom:
        generator.config['exclusions']['custom'] = [item.strip() for item in args.exclude_custom.split(',') if item.strip()]
    
    output_dir = Path(args.out)
    
    # Limiter le nombre d'articles si spécifié
    if args.count and args.count < len(topics):
        topics = topics[:args.count]
        if args.verbose:
            print(f"📊 Limitation à {args.count} articles")
    
    print(f"🎯 Thématique: {generator.config['theme']}")
    print(f"👥 Public: {generator.config['target_audience']}")
    print(f"📝 Ton: {generator.config['tone']}")
    if args.domain:
        print(f"🌐 Domaine: {generator.config['domain']}")
    if any(generator.config['exclusions'].values()):
        print(f"🚫 Exclusions activées")
    print(f"📄 Articles à générer: {len(topics)}")
    print()
    
    # Mesurer le temps si demandé
    import time
    start_time = time.time() if args.time else None
    
    # Traiter chaque sujet
    success_count = 0
    for i, topic in enumerate(topics, 1):
        try:
            if args.verbose:
                print(f"🔄 Génération {i}/{len(topics)}: {topic}")
            else:
                print(f"🔄 Génération: {topic}")
            
            data = generator.generate_content(topic, args.level)
            
            if data:
                filename = generator.save_content(data, output_dir)
                if args.verbose:
                    print(f"✓ Fichier créé: {args.out}/{filename}")
                    if 'exclusions' in str(generator._build_exclusions_text()).lower():
                        print(f"  🚫 Exclusions appliquées")
                else:
                    print(f"✓ Généré: {args.out}/{filename}")
                success_count += 1
                
        except Exception as e:
            print(f"✗ Échec sur \"{topic}\": {e}")
            if args.verbose:
                import traceback
                print(f"  📋 Détails: {traceback.format_exc()}")
    
    # Afficher le résumé avec temps si demandé
    elapsed_time = time.time() - start_time if start_time else None
    
    print(f"\n📊 Résumé: {success_count}/{len(topics)} articles générés")
    if elapsed_time:
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        print(f"⏱️  Temps d'exécution: {minutes}m {seconds}s")
    
    # Génération HTML si demandée
    if args.output_html and success_count > 0:
        print(f"\n🎨 Génération HTML non implémentée dans cette version")
        print(f"💡 Les articles JSON sont prêts dans {args.out}/")
        print(f"   Utilisez un script séparé pour convertir en HTML")

if __name__ == "__main__":
    main()