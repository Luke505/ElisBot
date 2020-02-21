# -*- coding: utf-8 -*-
class Config:
    token_bot       =   'TO EDIT'

    dbUser          =   'TO EDIT'
    dbPassword      =   'TO EDIT'
    dbName          =   'TO EDIT'
    dbHost          =   'TO EDIT'

    admins          =   [
        000000000       # Telegram user ID
    ]

    welcome         =   (
#        'Welcome to the Elis bot!\n'
#        'You can use:\n'
#        '/id   to look for a resident by his ID\n'
#        '/name to look for a resident by his NAME\n'
#        '/room to look for residents by their ROOM\n'
#        '/job  to look for residents by their JOB'
        'Benvenuto nell\'Elis bot!\n'
        'Puoi utilizzare:\n'
        '/id   per cercare un residente tramite la sigla\n'
        '/name per cercare un residente tramite il nome\n'
        '/room per cercare residenti di una camera\n'
        '/job  per cercare residenti in base al loro lavoro'
    )

    update          =   'Sono stato aggiornato! Invia /start per aggiornare!'#'I have been updated! Send /start to update!'

    commands        =   [
        '/id',
        '/name',
        '/room',
        '/job'
    ]

    debug           =   False

class Messages:
#    typeID          =   'Type the ID to search'
#    typeName        =   'Type the NAME to search'
#    typeRoom        =   'Type the ROOM to search'
#    typeJob         =   'Type the JOB to search'
#    typeUpdate      =   'Send the file with the queries to be executed'
#    roomHead        =   'Room Head'
#    areaHead        =   'Area Head'
#    jobManager      =   'Manager'
#    noID            =   'The ID does not exist!'
#    noName          =   'Resident not found!'
#    noRoom          =   'The ROOM does not exist!'
#    noJob           =   'The JOB does not exist!'
#    updated         =   'Update successful!'
#    unknowCMD       =   'Unknown command!'
    typeID          =   'Digita la sigla da cercare'
    typeName        =   'Digita il nome da cercare'
    typeRoom        =   'Digita la camera da cercare'
    typeJob         =   'Digita il lavoro da cercare'
    typeUpdate      =   'Invia il file con le query da eseguire'
    roomHead        =   'Capo Stanza'
    areaHead        =   'Capo Nucleo'
    jobManager      =   'Capo Incarico'
    noID            =   'La sigla non esiste!'
    noName          =   'Residente non trovato!'
    noRoom          =   'La camera non esiste!'
    noJob           =   'Il lavoro non esiste!'
    updated         =   'Aggiornamento eseguito con successo!'
    unknowCMD       =   'Comando sconosciuto!'
    face            =   {
        'default': '👦'.decode('utf-8'),      # 👦
        'roomHead': '👨'.decode('utf-8'),     # 👨
        'areaHead': '🧔'.decode('utf-8'),     # 🧔
        'manager': '🧔'.decode('utf-8')       # 🧔
    }
    icons           =   {
        'mailbox': '📫'.decode('utf-8'),      # 📫
        'telephone': '📞'.decode('utf-8'),    # 📞
        'books': '📚'.decode('utf-8'),        # 📚
        'hotel': '🏨'.decode('utf-8'),        # 🏨
        'ticket': '🎫'.decode('utf-8')        # 🎫
    } 