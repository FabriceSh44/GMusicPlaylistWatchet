# GMusicPlaylistWatcher
Persist google music playlist in a local file and compare the previous run to current playlist state

Usage :

    PlaylistScraperRunner.py [path to config.ini]

Content of config.ini :

    [GmailAccountInfo]
    gmailEmail = *gmail account*
    gmailAppPassword = *app password*
    
    [Persistence]
    dumpFile = *dump file destination*
