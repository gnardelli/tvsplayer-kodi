# -*- coding: utf-8 -*-
"""Kodi strings.po: adds the new strings to en_gb / it_it and writes fr, de, es, pt, pl, zh, ja.

python tools/po.py   (from the project root)
To add a string: put it in NEW (English, Italian) and at the same position in every list of T.
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
LANG = os.path.join(HERE, "..", "plugin.video.tvsplayer", "resources", "language")

NEW = {
    30042: ("Poor internet connection: the channel may not start",
            "Connessione internet debole: il canale potrebbe non partire"),
    30043: ("TV channels of this playlist", "Canali TV di questa playlist"),
    30044: ("Radio stations of this playlist", "Radio di questa playlist"),
    30045: ("TVS Player in the browser and on Android", "TVS Player nel browser e su Android"),
    30046: ("Your playlists and radio also in any web browser, nothing to install: https://tvsplayer.app\n"
            "On Android phones and tablets: TVS Player (free) and TVS Player Pro (TV guide, rewind, recordings) on Google Play.",
            "Le tue playlist e la radio anche in qualsiasi browser, senza installare niente: https://tvsplayer.app\n"
            "Su telefoni e tablet Android: TVS Player (gratis) e TVS Player Pro (guida TV, replay, registrazioni) su Google Play."),
}

# Same order as resource.language.en_gb/strings.po
T = {
    "fr": ["TV", "Radio", "Favoris", "Playlists", "Rechercher", "Toutes", "Ajouter une playlist M3U (adresse web)",
           "Ajouter une playlist M3U (fichier)", "Ajouter des radios gratuites par pays", "Adresse de la playlist (http://… .m3u)",
           "Nom de la playlist", "Contenu de cette playlist", "Automatique (TV et radio)", "TV seulement", "Radio seulement",
           "Chargement…", "{1} : {0} chaînes", "Impossible de charger la playlist", "Actualiser", "Supprimer",
           "Supprimer « {0} » ? Ses chaînes sont retirées. Les favoris restent.", "Ajouter aux favoris", "Retirer des favoris",
           "Choisir le lien", "Lien {0}", "Chaîne non disponible (aucun lien ne fonctionne)",
           "Aucune chaîne : ajoutez votre playlist M3U dans Playlists", "Radios de…",
           "Charger maintenant les radios gratuites ? (Radio Browser, un annuaire ouvert)",
           "TVS Player ne fournit aucune chaîne TV. Ajoutez seulement des playlists que vous avez le droit d’utiliser.",
           "{0} chaînes · mise à jour {1}", "Ajouté aux favoris", "Monter", "Descendre", "Rechercher chaînes et radios",
           "jamais", "Quel lien ?", "{0} liens", "Aucune chaîne trouvée : est-ce une playlist M3U ?",
           "L’adresse doit commencer par http:// ou https://", "Radios – {0}",
           "Connexion internet faible : la chaîne risque de ne pas démarrer", "Chaînes TV de cette playlist",
           "Radios de cette playlist", "TVS Player dans le navigateur et sur Android",
           "Vos playlists et la radio aussi dans n’importe quel navigateur, sans rien installer : https://tvsplayer.app/fr/\n"
           "Sur téléphones et tablettes Android : TVS Player (gratuit) et TVS Player Pro (guide TV, retour en arrière, enregistrements) sur Google Play.",
           "Général", "Vérifier les liens avant la lecture (ignorer ceux qui ne marchent pas)",
           "Délai de vérification des liens (secondes)", "Radios à charger par pays", "Premier démarrage effectué"],
    "de": ["TV", "Radio", "Favoriten", "Playlists", "Suchen", "Alle", "M3U-Playlist hinzufügen (Webadresse)",
           "M3U-Playlist hinzufügen (Datei)", "Kostenlose Radiosender nach Land hinzufügen", "Adresse der Playlist (http://… .m3u)",
           "Name der Playlist", "Inhalt dieser Playlist", "Automatisch (TV und Radio)", "Nur TV", "Nur Radio",
           "Wird geladen…", "{1}: {0} Sender", "Die Playlist konnte nicht geladen werden", "Aktualisieren", "Löschen",
           "„{0}“ löschen? Die Sender werden entfernt. Favoriten bleiben.", "Zu Favoriten hinzufügen", "Aus Favoriten entfernen",
           "Link wählen", "Link {0}", "Sender nicht verfügbar (kein funktionierender Link)",
           "Noch keine Sender: füge deine M3U-Playlist unter Playlists hinzu", "Radiosender aus…",
           "Jetzt kostenlose Radiosender laden? (Radio Browser, ein offenes Verzeichnis)",
           "TVS Player stellt keine TV-Sender bereit. Füge nur Playlists hinzu, die du nutzen darfst.",
           "{0} Sender · aktualisiert {1}", "Zu Favoriten hinzugefügt", "Nach oben", "Nach unten", "Sender und Radio suchen",
           "nie", "Welcher Link?", "{0} Links", "Keine Sender gefunden: ist das eine M3U-Playlist?",
           "Die Adresse muss mit http:// oder https:// beginnen", "Radiosender – {0}",
           "Schwache Internetverbindung: der Sender startet möglicherweise nicht", "TV-Sender dieser Playlist",
           "Radiosender dieser Playlist", "TVS Player im Browser und auf Android",
           "Deine Playlists und das Radio auch in jedem Browser, ohne Installation: https://tvsplayer.app/de/\n"
           "Auf Android-Handys und -Tablets: TVS Player (kostenlos) und TVS Player Pro (TV-Guide, Zurückspulen, Aufnahmen) bei Google Play.",
           "Allgemein", "Links vor der Wiedergabe prüfen (defekte überspringen)", "Zeitlimit der Linkprüfung (Sekunden)",
           "Radiosender pro Land", "Erster Start erledigt"],
    "es": ["TV", "Radio", "Favoritos", "Listas", "Buscar", "Todos", "Añadir lista M3U (dirección web)",
           "Añadir lista M3U (archivo)", "Añadir radios gratuitas por país", "Dirección de la lista (http://… .m3u)",
           "Nombre de la lista", "Contenido de esta lista", "Automático (TV y radio)", "Solo TV", "Solo radio",
           "Cargando…", "{1}: {0} canales", "No se ha podido cargar la lista", "Actualizar", "Eliminar",
           "¿Eliminar «{0}»? Se quitan sus canales. Los favoritos se quedan.", "Añadir a favoritos", "Quitar de favoritos",
           "Elegir enlace", "Enlace {0}", "Canal no disponible (ningún enlace funciona)",
           "Aún no hay canales: añade tu lista M3U en Listas", "Radios de…",
           "¿Cargar ahora las radios gratuitas? (Radio Browser, un directorio abierto)",
           "TVS Player no ofrece canales de TV. Añade solo listas que tengas derecho a usar.",
           "{0} canales · actualizada {1}", "Añadido a favoritos", "Subir", "Bajar", "Buscar canales y radios",
           "nunca", "¿Qué enlace?", "{0} enlaces", "No se han encontrado canales: ¿es una lista M3U?",
           "La dirección debe empezar por http:// o https://", "Radios – {0}",
           "Conexión a internet débil: puede que el canal no arranque", "Canales de TV de esta lista",
           "Radios de esta lista", "TVS Player en el navegador y en Android",
           "Tus listas y la radio también en cualquier navegador, sin instalar nada: https://tvsplayer.app/es/\n"
           "En móviles y tablets Android: TVS Player (gratis) y TVS Player Pro (guía TV, retroceder, grabaciones) en Google Play.",
           "General", "Comprobar los enlaces antes de reproducir (saltar los que no funcionan)",
           "Tiempo máximo de comprobación (segundos)", "Radios que cargar por país", "Primer inicio hecho"],
    "pt": ["TV", "Rádio", "Favoritos", "Listas", "Pesquisar", "Todos", "Adicionar lista M3U (endereço web)",
           "Adicionar lista M3U (ficheiro)", "Adicionar rádios gratuitas por país", "Endereço da lista (http://… .m3u)",
           "Nome da lista", "Conteúdo desta lista", "Automático (TV e rádio)", "Só TV", "Só rádio",
           "A carregar…", "{1}: {0} canais", "Não foi possível carregar a lista", "Atualizar", "Eliminar",
           "Eliminar «{0}»? Os canais são removidos. Os favoritos ficam.", "Adicionar aos favoritos", "Remover dos favoritos",
           "Escolher ligação", "Ligação {0}", "Canal indisponível (nenhuma ligação funciona)",
           "Ainda não há canais: adicione a sua lista M3U em Listas", "Rádios de…",
           "Carregar agora as rádios gratuitas? (Radio Browser, um diretório aberto)",
           "O TVS Player não fornece canais de TV. Adicione apenas listas que tem o direito de usar.",
           "{0} canais · atualizada {1}", "Adicionado aos favoritos", "Mover para cima", "Mover para baixo",
           "Pesquisar canais e rádios", "nunca", "Que ligação?", "{0} ligações", "Nenhum canal encontrado: é uma lista M3U?",
           "O endereço tem de começar por http:// ou https://", "Rádios – {0}",
           "Ligação à internet fraca: o canal pode não arrancar", "Canais de TV desta lista", "Rádios desta lista",
           "TVS Player no navegador e no Android",
           "As suas listas e a rádio também em qualquer navegador, sem instalar nada: https://tvsplayer.app/pt/\n"
           "Em telemóveis e tablets Android: TVS Player (gratuito) e TVS Player Pro (guia de TV, recuar, gravações) no Google Play.",
           "Geral", "Verificar as ligações antes de reproduzir (saltar as que não funcionam)",
           "Tempo máximo da verificação (segundos)", "Rádios a carregar por país", "Primeiro arranque feito"],
    "pl": ["TV", "Radio", "Ulubione", "Playlisty", "Szukaj", "Wszystkie", "Dodaj playlistę M3U (adres internetowy)",
           "Dodaj playlistę M3U (plik)", "Dodaj darmowe stacje radiowe według kraju", "Adres playlisty (http://… .m3u)",
           "Nazwa playlisty", "Zawartość tej playlisty", "Automatycznie (TV i radio)", "Tylko TV", "Tylko radio",
           "Ładowanie…", "{1}: {0} kanałów", "Nie udało się wczytać playlisty", "Odśwież", "Usuń",
           "Usunąć „{0}”? Jej kanały zostaną usunięte. Ulubione zostają.", "Dodaj do ulubionych", "Usuń z ulubionych",
           "Wybierz link", "Link {0}", "Kanał niedostępny (żaden link nie działa)",
           "Brak kanałów: dodaj swoją playlistę M3U w Playlistach", "Stacje radiowe z…",
           "Wczytać teraz darmowe stacje radiowe? (Radio Browser, otwarty katalog)",
           "TVS Player nie dostarcza kanałów TV. Dodawaj tylko playlisty, z których masz prawo korzystać.",
           "{0} kanałów · aktualizacja {1}", "Dodano do ulubionych", "W górę", "W dół", "Szukaj kanałów i radia",
           "nigdy", "Który link?", "{0} linków", "Nie znaleziono kanałów: czy to playlista M3U?",
           "Adres musi zaczynać się od http:// lub https://", "Stacje radiowe – {0}",
           "Słabe połączenie z internetem: kanał może się nie uruchomić", "Kanały TV z tej playlisty",
           "Stacje radiowe z tej playlisty", "TVS Player w przeglądarce i na Androidzie",
           "Twoje playlisty i radio także w każdej przeglądarce, bez instalowania: https://tvsplayer.app/pl/\n"
           "Na telefonach i tabletach z Androidem: TVS Player (za darmo) i TVS Player Pro (program TV, cofanie, nagrania) w Google Play.",
           "Ogólne", "Sprawdzaj linki przed odtworzeniem (pomijaj niedziałające)", "Limit czasu sprawdzania linków (sekundy)",
           "Liczba stacji radiowych na kraj", "Pierwsze uruchomienie wykonane"],
    "zh": ["电视", "电台", "收藏", "播放列表", "搜索", "全部", "添加 M3U 播放列表（网址）", "添加 M3U 播放列表（文件）",
           "按国家添加免费电台", "播放列表地址（http://… .m3u）", "播放列表名称", "此播放列表的内容", "自动（电视和电台）",
           "仅电视", "仅电台", "正在加载…", "{1}：{0} 个频道", "无法加载播放列表", "刷新", "删除",
           "删除“{0}”？其频道将被移除，收藏会保留。", "添加到收藏", "从收藏中移除", "选择链接", "链接 {0}",
           "频道不可用（没有可用的链接）", "还没有频道：请在“播放列表”中添加你的 M3U 播放列表", "电台所在国家…",
           "现在加载免费电台吗？（Radio Browser，一个开放目录）", "TVS Player 不提供任何电视频道。请只添加你有权使用的播放列表。",
           "{0} 个频道 · 更新于 {1}", "已添加到收藏", "上移", "下移", "搜索频道和电台", "从未", "哪个链接？", "{0} 个链接",
           "未找到频道：这是 M3U 播放列表吗？", "地址必须以 http:// 或 https:// 开头", "电台 – {0}",
           "网络连接较差：频道可能无法播放", "此播放列表的电视频道", "此播放列表的电台", "浏览器和 Android 上的 TVS Player",
           "在任何浏览器中也能使用你的播放列表和电台，无需安装：https://tvsplayer.app/zh/\n"
           "Android 手机和平板：Google Play 上的 TVS Player（免费）和 TVS Player Pro（电视指南、回看、录制）。",
           "常规", "播放前检查链接（跳过无法播放的链接）", "链接检查超时（秒）", "每个国家加载的电台数量", "已完成首次启动"],
    "ja": ["テレビ", "ラジオ", "お気に入り", "プレイリスト", "検索", "すべて", "M3U プレイリストを追加（Web アドレス）",
           "M3U プレイリストを追加（ファイル）", "国別に無料ラジオ局を追加", "プレイリストのアドレス（http://… .m3u）",
           "プレイリストの名前", "このプレイリストの内容", "自動（テレビとラジオ）", "テレビのみ", "ラジオのみ", "読み込み中…",
           "{1}：{0} チャンネル", "プレイリストを読み込めませんでした", "更新", "削除",
           "「{0}」を削除しますか？チャンネルは削除されます。お気に入りは残ります。", "お気に入りに追加", "お気に入りから削除",
           "リンクを選択", "リンク {0}", "チャンネルを利用できません（動作するリンクがありません）",
           "チャンネルがありません：「プレイリスト」で M3U プレイリストを追加してください", "ラジオ局の国…",
           "今すぐ無料ラジオ局を読み込みますか？（オープンなディレクトリ Radio Browser）",
           "TVS Player はテレビチャンネルを提供しません。利用する権利のあるプレイリストだけを追加してください。",
           "{0} チャンネル · 更新 {1}", "お気に入りに追加しました", "上へ移動", "下へ移動", "チャンネルとラジオを検索", "なし",
           "どのリンク？", "{0} 件のリンク", "チャンネルが見つかりません：M3U プレイリストですか？",
           "アドレスは http:// または https:// で始まる必要があります", "ラジオ局 – {0}",
           "インターネット接続が不安定です：チャンネルが開始できない可能性があります", "このプレイリストのテレビチャンネル",
           "このプレイリストのラジオ局", "ブラウザと Android の TVS Player",
           "インストール不要で、どのブラウザでもプレイリストとラジオを使えます：https://tvsplayer.app/ja/\n"
           "Android スマホとタブレット：Google Play の TVS Player（無料）と TVS Player Pro（番組表、巻き戻し、録画）。",
           "一般", "再生前にリンクを確認（動作しないリンクをスキップ）", "リンク確認のタイムアウト（秒）",
           "国ごとに読み込むラジオ局の数", "初回起動済み"],
}
FOLDER = {"fr": "fr_fr", "de": "de_de", "es": "es_es", "pt": "pt_pt", "pl": "pl_pl", "zh": "zh_cn", "ja": "ja_jp"}
CODE = {"fr": "fr_FR", "de": "de_DE", "es": "es_ES", "pt": "pt_PT", "pl": "pl_PL", "zh": "zh_CN", "ja": "ja_JP"}
ENTRY = re.compile(r'msgctxt "#(\d+)"\nmsgid "((?:[^"\\]|\\.)*)"\nmsgstr "((?:[^"\\]|\\.)*)"')


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def po(folder):
    return os.path.join(LANG, "resource.language." + folder, "strings.po")


def main():
    # 1. New strings in English and Italian, before the settings block (#30100)
    for folder, idx in (("en_gb", 0), ("it_it", 1)):
        text = io.open(po(folder), encoding="utf-8").read()
        have = {int(k) for k, _i, _s in ENTRY.findall(text)}
        add = "".join('msgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n\n' % (k, esc(v[0]), "" if idx == 0 else esc(v[1]))
                      for k, v in sorted(NEW.items()) if k not in have)
        if add:
            io.open(po(folder), "w", encoding="utf-8", newline="\n").write(
                text.replace('msgctxt "#30100"', add + 'msgctxt "#30100"', 1))
    # 2. The other languages, complete
    text = io.open(po("en_gb"), encoding="utf-8").read()
    items = ENTRY.findall(text)
    header = text[:text.index("msgctxt")]
    for lang, tr in T.items():
        assert len(tr) == len(items), (lang, len(tr), len(items))
        out = re.sub(r"Language: \w+", "Language: " + CODE[lang], header)
        for (k, msgid, _s), s in zip(items, tr):
            for ph in re.findall(r"\{\d\}", msgid):
                assert ph in s, (lang, k, ph)
            out += 'msgctxt "#%s"\nmsgid "%s"\nmsgstr "%s"\n\n' % (k, msgid, esc(s))
        d = os.path.dirname(po(FOLDER[lang]))
        if not os.path.isdir(d):
            os.makedirs(d)
        io.open(po(FOLDER[lang]), "w", encoding="utf-8", newline="\n").write(out.rstrip("\n") + "\n")
        print(lang, len(tr), "strings")


if __name__ == "__main__":
    main()
