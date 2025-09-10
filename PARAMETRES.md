# 📋 Liste complète des paramètres

## ⚙️ **Paramètres principaux**

| Paramètre | Type | Défaut | Description | Exemple |
|-----------|------|--------|-------------|---------|
| `--config` | string | `config_theme.ini` | Fichier de configuration thématique | `--config config_jardinage.ini` |
| `--theme` | string | - | Thème principal de génération | `--theme "Jardinage en hiver"` |
| `--count` | int | `5` | Nombre d'articles à générer | `--count 10` |
| `--topics` | list | - | Sujets spécifiques (sinon topics.txt) | `--topics "Sujet 1" "Sujet 2"` |
| `--level` | choice | `intermédiaire` | Niveau: débutant/intermédiaire/avancé | `--level avancé` |
| `--out` | string | `out` | Répertoire de sortie | `--out articles` |

## 🎨 **Paramètres de personnalisation**

| Paramètre | Type | Défaut | Description | Exemple |
|-----------|------|--------|-------------|---------|
| `--domain` | string | - | Nom de domaine du site | `--domain "monsite.fr"` |
| `--exclude-brands` | string | - | Marques à exclure (séparées par ,) | `--exclude-brands "Nike,Adidas"` |
| `--exclude-cities` | string | - | Villes à exclure (séparées par ,) | `--exclude-cities "Paris,Lyon"` |
| `--exclude-competitors` | string | - | Concurrents à exclure (séparées par ,) | `--exclude-competitors "site1.fr,site2.com"` |
| `--exclude-custom` | string | - | Mots/expressions à exclure (séparés par ,) | `--exclude-custom "mot1,expression2"` |

## 🔧 **Paramètres utilitaires**

| Paramètre | Type | Défaut | Description | Utilisation |
|-----------|------|--------|-------------|-------------|
| `--verbose` | flag | `False` | Mode verbeux avec détails | Debug et validation |
| `--time` | flag | `False` | Mesure le temps d'exécution | Optimisation performance |
| `--output-html` | flag | `False` | Prépare pour génération HTML | Développement futur |
| `--init-config` | flag | `False` | Crée fichier config par défaut | Configuration initiale |

## 🚀 **Commandes types**

### Génération rapide (développement)
```bash
python content_generator_generic.py \
  --config config_jardinage.ini \
  --theme "Test rapide" \
  --count 1 \
  --verbose \
  --time
```

### Production standard
```bash
python content_generator_generic.py \
  --config config_jardinage.ini \
  --theme "Jardinage d'automne" \
  --count 8 \
  --domain "monjardin.fr"
```

### Maximum de personnalisation
```bash
python content_generator_generic.py \
  --config config_cuisine.ini \
  --theme "Cuisine traditionnelle" \
  --count 12 \
  --domain "cuisine-authentique.fr" \
  --exclude-brands "McDo,KFC,Quick" \
  --exclude-competitors "Marmiton,750g" \
  --exclude-custom "industriel,transformé" \
  --verbose \
  --time
```

## 📊 **Sortie du programme**

### Mode normal
```
🎯 Thématique: Jardinage en hiver
👥 Public: jardiniers amateurs et passionnés  
📝 Ton: bienveillant et expert
📄 Articles à générer: 5

🔄 Génération: Sujet 1
✓ Généré: out/20250910-sujet-1.json
...
📊 Résumé: 5/5 articles générés
```

### Mode verbose + time
```
🎯 Thématique: Jardinage en hiver
👥 Public: jardiniers amateurs et passionnés
📝 Ton: bienveillant et expert  
🌐 Domaine: monjardin.fr
🚫 Exclusions activées
📄 Articles à générer: 3

🔄 Génération 1/3: Sujet 1
✓ Fichier créé: out/20250910-sujet-1.json
  🚫 Exclusions appliquées
...
📊 Résumé: 3/3 articles générés
⏱️  Temps d'exécution: 2m 34s
```

## ⚠️ **Gestion d'erreurs**

### Mode normal
```
✗ Échec sur "Sujet problématique": API Error
```

### Mode verbose  
```
✗ Échec sur "Sujet problématique": API Error
  📋 Détails: [Stack trace complète]
```

## 💡 **Bonnes pratiques**

1. **Développement** : Utilisez `--count 1 --verbose --time`
2. **Test exclusions** : Vérifiez avec `--verbose` 
3. **Production** : Optimisez avec `--time` périodiquement
4. **Debug** : `--verbose` pour identifier les problèmes
5. **Performance** : Limitez `--count` selon ressources API