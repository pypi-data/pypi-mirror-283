"""
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""

from ...messages import Lang
from .args_macros_classes import ArgConfig, MacroConfig, VAR_ARGS




PY_GLOBAL = MacroConfig(
    '',
    ArgConfig(
        'py_name', str, default="", index=0,
        docs = "Chemin relatif (sans l'extension du fichier) vers le fichier `{exo}.py` et les "
               "éventuels autres fichiers annexes, sur lesquels baser l'IDE.",
    ),
    ArgConfig(
        'ID', int, in_config=False, docs_type="None|int",
        docs="À utiliser pour différencier deux IDEs utilisant les mêmes fichiers [{{annexes()}}]"
             "(--ide-files), afin de différencier leurs sauvegardes (nota: $ID \\ge 0$)."
    ),
    ArgConfig(
        'SANS', str, default="",
        docs = "Pour interdire des fonctions builtins, des méthodes ou des modules : chaîne de "
               "noms séparés par des virgules et/ou espaces."
    ),
    ArgConfig(
        'WHITE', str, default="",
        docs = "(_\"White list\"_) Ensemble de noms de modules/packages à pré-importer avant que "
               "les interdictions ne soient mises en place (voir argument `SANS` ; `WHITE` _est "
               "normalement {{ orange('**obsolète**') }}_)."
    ),
    ArgConfig(
        'REC_LIMIT', int, default=-1,
        docs = "Pour imposer une profondeur de récursion maximale. Nota: ne jamais descendre en-"
               "dessous de 20. La valeur par défaut, `#!py -1`, signifie que l'argument n'est pas "
               "utilisé."
    ),
)




MOST_LIKELY_USELESS_ID = PY_GLOBAL.ID.copy_with(
    docs="À utiliser pour différencier deux appels de macros différents, dans le cas où vous "
         "tomberiez sur une collision d'id (très improbable, car des hachages sont utilisés. "
         "Cet argument ne devrait normalement pas être nécessaire pour cette macro)."
)

def _py_globals_copy_gen(py_name_replacement:ArgConfig):
    return (
        MOST_LIKELY_USELESS_ID if name=='ID'
        else py_name_replacement if name=='py_name'
        else arg.copy_with()
        for name,arg in PY_GLOBAL.args.items()
    )





#----------------------------------------------------------------------------------------






IDE = MacroConfig(
    'IDE',
    *PY_GLOBAL.args.values(),
    ArgConfig(
        'MAX', int, default=5, docs_type="int|'+'",
        deprecated_source = 'ides.max_attempts_before_corr_available',
        docs = "Nombre maximal d'essais de validation avant de rendre la correction et/ou les "
               "remarques disponibles."
    ),
    ArgConfig(
        'LOGS', bool, default=True,
        deprecated_source = 'ides.show_assertion_code_on_failed_test',
        docs = "{{ red('Durant des tests de validation') }}, si LOGS est `True`, le code "
               "complet d'une assertion est utilisé comme message d'erreur, quand "
               "l'assertion a été écrite sans message."
    ),
    ArgConfig(
        'MAX_SIZE', int, default=30,
        deprecated_source = 'ides.default_ide_height_lines',
        docs = "Impose la hauteur maximale possible pour un éditeur, en nombres de lignes."
    ),
    ArgConfig(
        'TERM_H', int, default=10,
        deprecated_source = 'ides.default_height_ide_term',
        docs = "Impose le nombre de lignes du terminal."
    ),
)






TERMINAL = MacroConfig(
    'terminal',
    *_py_globals_copy_gen( PY_GLOBAL.py_name.copy_with(
        docs = "Crée un terminal isolé utilisant le fichier python correspondant (sections "
               "autorisées: `env`, `env_term`, `post_term`, `post` et `ignore`)."
    )),
    ArgConfig(
        'TERM_H', int, default=10,
        deprecated_source = 'ides.default_height_isolated_term',
        docs = "Impose le nombre de lignes du terminal."
    ),
    ArgConfig(
        'FILL', str, default='', ide_link=False,
        docs = "Commande à afficher dans le terminal lors de sa création.<br>{{red('Uniquement "
               "pour les terminaux isolés.')}}"
    ),
)






PY_BTN = MacroConfig(
    'py_btn',
    *( arg.copy_with(in_docs = arg.name in ('py_name', 'ID'))
       for arg in _py_globals_copy_gen( PY_GLOBAL.py_name.copy_with(
            docs="Crée un bouton isolé utilisant le fichier python correspondant (uniquement "
                "`env` et `ignore`)."
    ))),
    ArgConfig(
        'WRAPPER', str, default='div', ide_link=False,
        docs = "Type de balise dans laquelle mettre le bouton."
    ),
    ArgConfig(
        'HEIGHT', int, is_optional=True, ide_link=False, docs_type="None|int",
        docs = "Hauteur par défaut du bouton."
    ),
    ArgConfig(
        'WIDTH', int, is_optional=True, ide_link=False, docs_type="None|int",
        docs = "Largeur par défaut du bouton."
    ),
    ArgConfig(
        'SIZE', int, is_optional=True, ide_link=False, docs_type="None|int",
        docs = "Si défini, utilisé pour la largeur __et__ la hauteur du bouton."
    ),
    ArgConfig(
        'ICON', str, default="", ide_link=False,
        docs = "Par défaut, le bouton \"play\" des tests publics des IDE est utilisé."
               "<br>Peut également être une icône `mkdocs-material`, une adresse vers une image "
               "(lien ou fichier), ou du code html.<br>Si un fichier est utiliser, l'adresse doit "
               "être relative au `docs_dir` du site construit."
    ),
    ArgConfig(
        'TIP', str, default=Lang.py_btn.msg, ide_link=False,
        docs = "Message à utiliser pour l'info-bulle."
    ),
    ArgConfig(
        'TIP_SHIFT', int, default=50, ide_link=False,
        docs = "Décalage horizontal de l'info-bulle par rapport au bouton, en `%` (50% correspond "
        "à un centrage)."
    ),
    ArgConfig(
        'TIP_WIDTH', float, default=0.0, ide_link=False,
        docs = "Largeur de l'info-bulle, en `em` (`#!py 0` correspond à une largeur automatique)."
    ),
)






SECTION = MacroConfig(
    'section',

    # Required on the python side, but should never be given through "meta", so it has to be
    # non blocking on the config side:
    PY_GLOBAL.py_name.copy_with(
        docs="[Fichier python {{ annexe() }}](--ide-files).", ide_link=False,
    ),
    ArgConfig(
        'section', str, index=1, is_optional=True, ide_link=False,
        docs = "Nom de la section à extraire."
    ),
)






PY = MacroConfig(
    'py',

    # Required on the python side, but should never be given through "meta", so it has to be
    # non blocking on the config side:
    ArgConfig(
        'py_name', str, is_optional=True, index=0, ide_link=False,
        docs = "Fichier source à utiliser (sans l'extension)."
    ),
)






MULTI_QCM = MacroConfig(
    'multi_qcm',

    # Required on the python side, but should never be given through "meta": must not be blocking:
    ArgConfig(
        '*inputs', list, index=VAR_ARGS, in_config=False, docs_default_as_type=False, ide_link=False,
        docs = "Chaque argument individuel est une [liste décrivant une question avec ses choix "
               "et réponses](--qcm_question)."
    ),
    ArgConfig(
        'hide', bool, default=False, ide_link=False,
        docs = "Si `#!py True`, un masque apparaît au-dessus des boutons pour signaler à "
               "l'utilisateur que les réponses resteront cachées après validation."
    ),
    ArgConfig(
        'multi', bool, default=False, ide_link=False,
        docs = "Réglage pour toutes les questions du qcms ayant à ou un seul choix comme bonne "
               "réponse, indiquant si elles sont à choix simples ou multiples."
    ),
    ArgConfig(
        'shuffle', bool, default=False, ide_link=False,
        docs = "Mélange les questions et leurs choix ou pas, à chaque fois que le qcm est joué."
    ),
    ArgConfig(
        'admo_kind', str, default="!!!", ide_link=False,
        docs = "Type d'admonition dans laquelle les questions seront rassemblées (`'???'` et "
               "`'???+'` sont également utilisables, pour des qcms repliés ou \"dépliés\")."
    ),
    ArgConfig(
        'admo_class', str, default="tip", ide_link=False,
        docs ="Pour changer la classe d'admonition. Il est également possible d'ajouter d'autres "
              "classes si besoin, en les séparant par des espaces (ex: `#!py 'warning my-class'`)."
    ),
    ArgConfig(
        'qcm_title', str, default=Lang.qcm_title.msg, ide_link=False,
        docs = "Pour changer le titre de l'admonition."
    ),
    ArgConfig(
        'DEBUG', bool, default=False, ide_link=False,
        docs = "Si True, affiche dans la console le code markdown généré pour ce qcm."
    ),
)






ARGS_MACRO_CONFIG = MacroConfig.build_config_and_accessors(
    'args',
    IDE,
    TERMINAL,
    PY_BTN,
    SECTION,
    MULTI_QCM,
    PY,
)
