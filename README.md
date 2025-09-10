# 🚀 Générateur de Contenu Éditorial Multi-Thématique

Système avancé de génération d'articles thématiques avec maillage interne optimisé et design responsive.

## 📋 Fonctionnalités

- **Génération automatique** d'articles structurés à partir de thématiques
- **Maillage interne intelligent** avec liens contextuels naturels
- **Pages HTML responsive** avec design moderne
- **Fil d'ariane** et navigation optimisée
- **SEO avancé** avec métadonnées et Schema.org
- **Configuration flexible** via fichiers INI
- **Support multi-thématiques** (jardinage, cuisine, bricolage, etc.)

## 🛠️ Installation

### Prérequis
- Python 3.8+
- Clé API OpenAI

### Dépendances
```bash
pip install openai python-slugify markdown python-dotenv
```

### Configuration
1. Créez un fichier `.env` :
```bash
OPENAI_API_KEY=sk-proj-votre-clé-api-ici
OPENAI_MODEL=gpt-4o-mini
```

2. Configurez votre thématique dans un fichier `.ini` :
```ini
[site]
name = Mon Site
domain = monsite.fr
theme = Votre thématique
target_audience = votre public cible
tone = professionnel et accessible
content_type = guide pratique
expertise_level = expert dans le domaine

[seo]
internal_links_prefix = theme_
meta_author = Votre Nom
schema_org_type = HowTo

[generation]
min_words = 800
max_words = 1200
include_faq = true
internal_links_count = 6

[EXCLUSIONS]
# Marques à ne pas mentionner
brands = Nike, Adidas, Puma
# Villes à éviter de citer
cities = Paris, Lyon, Marseille
# Concurrents à ne pas nommer
competitors = concurrent1, concurrent2
# Mots/expressions personnalisés à exclure
custom = mot-interdit, expression-interdite
```

## 🚀 Utilisation

### Génération simple (5 articles par défaut)
```bash
python content_generator_generic.py \
  --config config_jardinage.ini \
  --theme "Jardinage en hiver"
```

### Génération avec nombre spécifique
```bash
python content_generator_generic.py \
  --config config_jardinage.ini \
  --theme "Jardinage en hiver" \
  --count 10
```

### Avec génération HTML
```bash
python content_generator_generic.py \
  --config config_jardinage.ini \
  --theme "Jardinage en hiver" \
  --count 10 \
  --output-html
```

### Avec domaine et exclusions
```bash
python content_generator_generic.py \
  --config config_jardinage.ini \
  --theme "Jardinage en hiver" \
  --count 10 \
  --domain "monjardin.fr" \
  --exclude-brands "Monsanto,Roundup" \
  --exclude-cities "Paris,Lyon" \
  --exclude-custom "pesticide,chimique"
```

### Mode verbeux avec mesure de temps
```bash
python content_generator_generic.py \
  --config config_cuisine.ini \
  --theme "Cuisine d'hiver" \
  --count 3 \
  --verbose \
  --time
```

### Options disponibles

#### Options principales
- `--config` : Fichier de configuration thématique (défaut: config_theme.ini)
- `--theme` : Thème principal de génération (ex: "Jardinage en hiver")
- `--count` : Nombre d'articles à générer (défaut: 5)
- `--topics` : Liste de sujets spécifiques (sinon utilise topics.txt)
- `--level` : Niveau de difficulté (débutant/intermédiaire/avancé)
- `--out` : Répertoire de sortie (défaut: out)

#### Personnalisation
- `--domain` : Nom de domaine du site (ex: monsite.fr)
- `--exclude-brands` : Marques à exclure (ex: "Nike,Adidas,Puma")
- `--exclude-cities` : Villes à exclure (ex: "Paris,Lyon,Marseille")
- `--exclude-competitors` : Concurrents à exclure
- `--exclude-custom` : Mots/expressions personnalisés à exclure

#### Utilitaires
- `--output-html` : Prépare pour génération HTML (en développement)
- `--verbose` : Mode verbeux avec détails
- `--time` : Mesure et affiche le temps d'exécution
- `--init-config` : Crée un fichier de configuration par défaut

## 📁 Structure générée

```
votre-projet/
├── content_generator_generic.py    # Script principal
├── config_[theme].ini             # Configuration thématique
├── .env                          # Variables d'environnement
├── [theme]_index.html            # Page d'accueil
├── [theme]_[article].html        # Pages d'articles
└── [theme]/                      # Données JSON
    └── *.json                    # Articles structurés
```

## 🎯 Exemple concret : Jardinage

### Commande
```bash
python content_generator_generic.py \
  --config config_jardinage.ini \
  --theme "Jardinage en hiver" \
  --count 10 \
  --output-html
```

### Résultat
- **Articles générés** selon le nombre spécifié (défaut: 5)
- **Domaine personnalisé** intégré automatiquement
- **Exclusions appliquées** aux contenus générés
- **Maillage interne** : 5-8 liens contextuels par article
- **SEO optimisé** avec métadonnées complètes
- **Mesure de temps** optionnelle pour performance
- **Mode verbeux** pour debug et validation

### Articles générés
1. Préparation du jardin pour l'hiver
2. Protection des plantes du gel et du froid
3. Plantation des bulbes de printemps
4. Entretien des outils de jardinage
5. Compostage pendant la saison froide
6. Plantes d'intérieur pour l'hiver
7. Planification du potager
8. Taille des arbres fruitiers
9. Semis sous abri

## 🔧 Personnalisation

### Nouvelles thématiques

#### Cuisine
```bash
# Créer config_cuisine.ini
python content_generator_generic.py \
  --config config_cuisine.ini \
  --theme "Cuisine d'hiver" \
  --count 8 \
  --output-html
```

#### Bricolage
```bash
# Créer config_bricolage.ini  
python content_generator_generic.py \
  --config config_bricolage.ini \
  --theme "Bricolage maison" \
  --count 12 \
  --output-html
```

#### Sport
```bash
# Créer config_sport.ini
python content_generator_generic.py \
  --config config_sport.ini \
  --theme "Fitness à domicile" \
  --count 15 \
  --output-html
```

## 📊 Structure des fichiers JSON

```json
{
  "title": "Titre de l'article",
  "slug": "titre-article",
  "seo_title": "Titre SEO optimisé",
  "seo_description": "Description pour les moteurs de recherche",
  "keywords": ["mot-clé1", "mot-clé2", "mot-clé3"],
  "content_markdown": "# Contenu en Markdown",
  "content_html": "<h1>Contenu converti en HTML</h1>",
  "faq_jsonld": {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [...]
  },
  "internal_links": ["/article1", "/article2", "/article3"]
}
```

## 📈 Caractéristiques techniques

### Articles générés
- **Contenu riche** : 800-1200 mots par article
- **SEO optimisé** : meta title, description, mots-clés
- **Schema.org JSON-LD** pour FAQ et HowTo
- **Maillage interne intelligent** : 5-8 liens contextuels par article

### Pages HTML
- **Design responsive** CSS moderne
- **Fil d'ariane** sur chaque page
- **Navigation optimisée** entre articles
- **Liens internes contextuels** intégrés naturellement
- **Meta tags** optimisés pour SEO
- **Structure sémantique** HTML5

### Performance
- **Génération rapide** : 4-5 minutes pour 10 articles
- **Maillage intelligent** : liens contextuels automatiques
- **Aucun lien cassé** : validation automatique
- **SEO optimisé** : métadonnées et structure

## 🔒 Sécurité

⚠️ **Important** : Utilisez un fichier `.env` pour vos clés API, ne les committez jamais dans Git.

- **Validation des entrées** pour éviter les injections
- **Gestion des erreurs** robuste
- **API calls** sécurisées avec gestion des timeouts
- **Variables d'environnement** pour les clés sensibles

## 📝 Licence

Projet privé - Tous droits réservés