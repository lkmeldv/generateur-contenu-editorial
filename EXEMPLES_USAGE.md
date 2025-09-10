# 📚 Exemples d'utilisation du générateur

## 🧪 Tests rapides

### Test 1 : Génération simple avec domaine personnalisé
```bash
python content_generator_generic.py \
  --config config_jardinage.ini \
  --topics "Taille des rosiers en hiver" \
  --domain "monjardin-passion.fr"
```

### Test 2 : Cuisine avec exclusions multiples
```bash
python content_generator_generic.py \
  --config config_cuisine.ini \
  --topics "Recettes d'hiver réconfortantes" \
  --domain "cuisine-maison.fr" \
  --exclude-brands "McDo,KFC,Burger King" \
  --exclude-competitors "Marmiton,750g" \
  --exclude-custom "malbouffe,industriel"
```

### Test 3 : Vérification des exclusions dans le prompt
Le script affichera dans le prompt système :

```
RESTRICTIONS ÉDITORIALES :
- INTERDIT de citer ces marques : McDo, KFC, Burger King
- INTERDIT de mentionner ces concurrents : Marmiton, 750g
- INTERDIT ces mots/expressions : malbouffe, industriel
```

## 🎯 Exemples par thématique

### Jardinage avec exclusions environnementales
```bash
python content_generator_generic.py \
  --config config_jardinage.ini \
  --topics "Jardinage bio sans produits chimiques" \
  --domain "jardin-ecologique.fr" \
  --exclude-brands "Monsanto,Bayer,Roundup" \
  --exclude-custom "pesticide chimique,engrais synthétique"
```

### Sport sans marques concurrentes
```bash
python content_generator_generic.py \
  --config config_sport.ini \
  --topics "Équipement running débutant" \
  --domain "sport-nature.fr" \
  --exclude-brands "Nike,Adidas,Puma" \
  --exclude-cities "Paris,Lyon,Marseille"
```

### Bricolage professionnel
```bash
python content_generator_generic.py \
  --config config_bricolage.ini \
  --topics "Rénovation salle de bain" \
  --domain "bricolage-expert.fr" \
  --exclude-competitors "Leroy Merlin,Castorama" \
  --exclude-brands "Bosch,Makita"
```

## 📋 Configuration avancée

### Fichier .ini complet avec exclusions
```ini
[THEME]
site_name = MonSiteExpert.fr
domain = monsite-expert.fr
theme = expertise spécialisée
target_audience = professionnels et experts
tone = technique et précis
content_type = guide expert
expertise_level = spécialiste reconnu
content_style = approche méthodique et détaillée

[EXCLUSIONS]
brands = concurrent1, concurrent2, marque-interdite
cities = ville-concurrence, autre-ville
competitors = site-concurrent.fr, autre-concurrent.com
custom = terme-interdit, expression-sensible, mot-tabou
```

## 🚨 Validation des exclusions

Pour vérifier que les exclusions fonctionnent :

1. **Lancez le script** avec les paramètres d'exclusion
2. **Vérifiez le prompt système** affiché (contient les restrictions)
3. **Contrôlez le contenu généré** (aucune mention des termes exclus)
4. **Testez différentes combinaisons** d'exclusions

## 💡 Bonnes pratiques

### Exclusions efficaces
- **Soyez spécifique** : "Nike Air Max" plutôt que "Nike"
- **Pensez aux variantes** : "McDo,McDonald's,McDonald"
- **Incluez les concurrents directs** dans votre secteur
- **Adaptez selon le public** (B2B vs B2C)

### Domaines cohérents
- **Utilisez des domaines réalistes** : "jardinage-pro.fr"
- **Évitez les extensions étranges** : préférez .fr, .com
- **Soyez cohérent** avec votre thématique

## 🔍 Débogage

Si les exclusions ne fonctionnent pas :

1. **Vérifiez la syntaxe** : virgules sans espaces excessifs
2. **Contrôlez le fichier .ini** : section [EXCLUSIONS] correcte
3. **Testez en CLI d'abord** avant le fichier de config
4. **Regardez le prompt système** généré pour validation