import xbmcgui,xbmcplugin

plugin_handle = int(sys.argv[1])
_id = 'plugin.video.MrSportTV'
_icondir = "special://home/addons/" + _id + "/logos/"

def add_video_item(url, infolabels, img=''):
    listitem = xbmcgui.ListItem(infolabels['title'], iconImage=img, thumbnailImage=img)
    listitem.setInfo('video', infolabels)
    listitem.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(plugin_handle, url, listitem, isFolder=False)

# Entertainment
add_video_item('plugin://program.plexus/?mode=1&url=acestream://c39db61fd585ebfa446983d0af9d9d637df9678c&mode=1&name=acestream&mode=1&name=SPORT TV 1',{ 'title': 'Sport TV 1'}, '%s/sport_tv1_pt.png'% _icondir)
add_video_item('plugin://program.plexus/?mode=2&url=http://content.torrent-tv.ru/YjZ5cTNmS2RMRFhsQStuNkRFQ2p4ZzJER2NmcVp2NkhKZG5oc0lXakxkK3JVc0k4NjkxOVBnVi9uZVZJeEZkbnROblkwd0VPOXhrUTlzUHMvcnJ2Y0E9PQ/10480.acelive&mode=1&name=acestream&mode=1&name=SPORT TV 1',{ 'title': 'Sport TV 1 (Stream 2'}, '%s/sport_tv1_pt.png'% _icondir)
add_video_item('plugin://program.plexus/?mode=1&url=acestream://ef6c2b73a0436e06478790e7f8f27f173159dd59&mode=1&name=acestream&mode=1&name=SPORT TV1',{ 'title': 'Sport TV 1 (Stream 3)'}, '%s/sport_tv1_pt.png'% _icondir)
add_video_item('plugin://program.plexus/?mode=1&url=acestream://cfeb62e9c104e669a639e74966ad9e6f4b1939b6&mode=1&name=acestream&mode=1&name=SPORT TV 1',{ 'title': 'Sport TV 1 (Stream 4'}, '%s/sport_tv1_pt.png'% _icondir)
add_video_item('plugin://program.plexus/?mode=1&url=acestream://a3776be8c08f52b3366c83fff09609721e28cd69&mode=1&name=acestream&mode=1&name=Sport TV2',{ 'title': 'Sport TV 2'}, '%s/sport_tv2_pt.png'% _icondir)
add_video_item('plugin://program.plexus/?mode=1&url=http://content.torrent-tv.ru/YjZ5cTNmS2RMRFhsQStuNkRFQ2p4ZzJER2NmcVp2NkhKZG5oc0lXakxkK3JVc0k4NjkxOVBnVi9uZVZJeEZkbnROblkwd0VPOXhrUTlzUHMvcnJ2Y0E9PQ/10481.acelive&mode=1&name=acestream&mode=1&name=Sport TV2',{ 'title': 'Sport TV 2 (Stream 2)'}, '%s/sport_tv2_pt.png'% _icondir)
add_video_item('plugin://program.plexus/?mode=1&url=acestream://24660dc5f5a642f7f5df8873ddac481bc4702115&mode=1&name=acestream&mode=1&name=Sport TV2',{ 'title': 'Sport TV 2 (Stream 3'}, '%s/sport_tv2_pt.png'% _icondir)
add_video_item('plugin://program.plexus/?mode=1&url=acestream://ed5acde0ca3f6092b278e4e705cdd1002ebb1ff2&mode=1&name=acestream&mode=1&name=Sport TV2',{ 'title': 'Sport TV 2 (Stream 4)'}, '%s/sport_tv2_pt.png'% _icondir)


xbmcplugin.endOfDirectory(plugin_handle)
xbmc.executebuiltin("Container.SetViewMode(500)")

