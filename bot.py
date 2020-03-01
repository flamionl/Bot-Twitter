from tweepy import *
from re import *
import credentials
import time
import random
#Authentification
auth = OAuthHandler(credentials.api_key, credentials.api_secret_key)
auth.set_access_token(credentials.access_token,credentials.access_token_secret)
api = API(auth)
#Mots clés de recherce des tweets
liste_recherche = ['#Concours','Gagne','RT + Follow']

def participation(keywords) :   
    """"Participe à des concours sur twitter
    Paramètre
    ---------
    keywords : mots clés utilisés pour la recherche de concours (list)
    """
    for word in keywords :
        print('Recherche avec le mot', word)
        for tweet in Cursor(api.search, q = word, tweet_mode = 'extended', lang = 'fr', result_type = 'mixed').items(30) :
            while retweet_concours_rate() >= 25 :
               	random_retweet()
               	print('Pause après retweet')
               	time.sleep(random.randint(300,500))
            while retweet_rate() >= 50 :
            	random_tweet()
            	print('Pause après tweet')
            	time.sleep(random.randint(300,500))
            #Si le tweet est un retweet
            if hasattr(tweet,'retweeted_status') :
                print('--------------------------------------------------------------------')
                print('Concours trouvé, auteur :', tweet.retweeted_status.author.screen_name)
                try :
                    #On RT
                    api.retweet(tweet.retweeted_status.id)
                    print('Retweet du tweet')
                    time.sleep(random.randrange(2,10))
                    #On fav
                    api.create_favorite(tweet.retweeted_status.id)
                    time.sleep(random.randrange(2,10))
                    print('Fav du tweet')
                    #On follow
                    api.create_friendship(tweet.retweeted_status.author.id)
                    time.sleep(random.randrange(2,10))
                    #Follow si besoin de follow des gens mentionnées dans le tweet
                    follow(tweet)
                    time.sleep(random.randrange(2,10))
                    #On commente avec le hashtag si besoin et on mentionne des amis
                    commentaire(tweet)
                    #On met un cool down de quelques minutes pour ne pas spam les requêtes
                    print('Cool down avant le changement de mot clé')
                    time.sleep(random.randint(600,800))
                except TweepError as err :
                    if err.api_code == 185 :
                        print('Trop de requêtes, programme en stand by pendant 20 minutes')
                        time.sleep(1250)
                    elif err.api_code == 139 or err.api_code == 327 or err.api_code == 160 :
                        pass
                    else :
                        print(err.reason)
            #Si le tweet n'est pas un retweet
            else :
                print('--------------------------------------------------------------------')
                print('Concours trouvé, auteur :', tweet.user.screen_name)
                try :
                    #On RT
                    api.retweet(tweet.id)
                    time.sleep(random.randrange(2,10))
                    print('Retweet du tweet')
                    #On fav
                    api.create_favorite(tweet.id)
                    time.sleep(random.randrange(2,10))
                    print('Fav du tweet')
                    #On follow
                    api.create_friendship(tweet.user.id)
                    time.sleep(random.randrange(2,10))
                    #Follow si besoin de follow des gens mentionnées dans le tweet
                    follow(tweet)
                    time.sleep(random.randrange(2,10))
                    #On commente avec le hashtag si besoin et on mentionne des amis
                    commentaire(tweet)
                    #On met un cool down  pour ne pas spam les requêtes
                    time.sleep(random.randrange(600,1000))
                except TweepError as err :
                    if err.api_code == 185 :
                        print('Trop de requêtes, programme en stand by pendant 20 minutes')
                        time.sleep(1250)
                    elif err.api_code == 139 or err.api_code == 327 or err.api_code == 160 or err.response == 326 :
                        pass
                    else :
                        print(err.reason)

def follow(tweet) :
    """Follow des gens mentionnés dans un tweet
    Paramètres
    ----------
    tweet : tweet où les gens sont mentionnés (objet)
    """
    try :
        #Si le tweet est un retweet
        if hasattr(tweet, 'retweeted_status') :
            #On parcourt le tweet et on follow à chaque @ trouvé
            words = tweet.retweeted_status.full_text.split()
            for word in words :
                if word.find('@') == 0 :
                    print('Compte à follow trouvé : ',word)
                    api.create_friendship(word)
        #Si le tweet est n'est pas un retweet
        else :
            #On parcourt le tweet et on follow à chaque @ trouvé
            words = tweet.full_text.split()
            for word in words :
                if word.find('@') == 0 :
                    print('Compte à follow trouvé : ',word)
                    api.create_friendship(word)
    except TweepError as err :
        if err.api_code == 226 or err.api_code == 185 :
            print('Trop de requêtes, programme en stand by pendant 20 minutes')
            time.sleep(1250)
        elif err.api_code == 139 or err.api_code == 327 or err.api_code == 160 or err.response == 326 :
            pass
        else :
            print(err.reason)

def commentaire(tweet) :
    """ Commente un tweet avec un hashtag lorsque demandé et mentionne des amis si demandé
    Paramètres
    ----------
    tweet : tweet où l'on demande de commenter avec un hashtag (objet)
    """
    #Liste de commentaires pour mentionner des amis
    comments_mention = ['Inshallah ça passe','On croise les doigts','Espérons que ça passe', " J'invite : ", " Hop Hop, j'invite : ",
               " Avec moi : ", " Help me : ", " Pour vous aussi les gars : ", " tentez votre chance ! : ",
               " Je tente ma chance ! J'espère que je vais gagner ! : ", " J'espère que vais gagner ! : ",
               " Merci pour le concours ! : ", " Que la chance soit avec moi ! et vous ",
               " Merci d'organiser ce concours ! Ça peut vous intéresser ", 
               " C'est pour vous ça ! : ", " Celui là on le gagne ",
               " Merci d'organiser ce concours ! ", " Bonne chance à tous ! ", 
               " J'ai tellement envie de gagner, essayez vous aussi ", " Je participe et j'invite "]

    index = random.randint(0,len(comments_mention)-1)
    #Liste de commentaires
    comments = ['Inshallah ça passe','On croise les doigts','Espérons que ça passe','Prions le seigneur','Merci pour le concours !','Merci d\'organiser ce concours','J\'aimerais trop gagner','si je gagne je vous fait un bisous']
    index_2 = random.randint(0,len(comments)-1)
    #Si le tweet est un retweet
    try :
        if hasattr(tweet,'retweeted_status') :
            words = tweet.retweeted_status.full_text.split()
            hashtag = ''
            #On cherche des hashtags
            for word in words : 
                if word.find('#') == 0 or word.find('#') == 1 or word.find('#') == 2 :
                    if 'concours' in word or 'Concours' in word or 'CONCOURS' in word or word =='#RT' or 'Follow' in word or 'follow' in word :
                        word = ''
                    hashtag = hashtag + ' ' + word
                    print('Hashtag trouvé :', word)
            #On parcourt le tweet à la recherche de mots clés pour voir si on doit tag des amis 
            if search("(?i)mentionne",tweet.retweeted_status.full_text) :
                print('Mot clé trouvé, mention des amis...')
                mention_amount(tweet,hashtag,comments_mention,index,index_2)
            elif search("(?i)invite", tweet.retweeted_status.full_text) :
                print('Mot clé trouvé, mention des amis...')
                mention_amount(tweet,hashtag,comments_mention,index,index_2)
            elif search("(?i)invitez", tweet.retweeted_status.full_text) :
                print('Mot clé trouvé, mention des amis...')
                mention_amount(tweet,hashtag,comments_mention,index,index_2) 
            elif search("(?i)tag",tweet.retweeted_status.full_text) :
                print('Mot clé trouvé, mention des amis...')
                mention_amount(tweet,hashtag,comments_mention,index,index_2)
            elif search("(?i)identifie",tweet.retweeted_status.full_text) :
                print('Mot clé trouvé, mention des amis...')
                mention_amount(tweet,hashtag,comments_mention,index,index_2)
            elif search("(?i)identifiez",tweet.retweeted_status.full_text) :
                print('Mot clé trouvé, mention des amis...')
                mention_amount(tweet,hashtag,comments_mention,index,index_2)
            elif search("(?i)tague",tweet.retweeted_status.full_text) :
                print('Mot clé trouvé, mention des amis...')
                mention_amount(tweet,hashtag,comments_mention,index,index_2)
            else :
                api.update_status('@'+tweet.retweeted_status.author.screen_name+' '+hashtag+' '+comments[index_2],tweet.retweeted_status.id)
                print('Commente le tweet, pas de mentions trouvées..')
        #Si le tweet n'est pas un retweet
        else :
            words = tweet.full_text.split()
            hashtag = ''
            #On cherche des hashtags
            for word in words : 
                if word.find('#') == 0 or word.find('#') == 1 or word.find('#') == 2 :
                    if 'concours' in word or 'Concours' in word or 'CONCOURS' in word or word =='#RT' or 'Follow' in word or 'follow' in word :
                        word = ''
                    hashtag = hashtag + ' ' + word
                    print('Hashtag trouvé :', word)
            #On parcourt le tweet à la recherche de mots clés pour voir si on doit tag des amis
            if search("(?i)mentionne",tweet.full_text) :
                print('Mot clé trouvé, mention des amis...')
                mention_amount(tweet,hashtag,comments_mention,index,index_2)
            elif search("(?i)invite", tweet.full_text) :
                print('Mot clé trouvé, mention des amis...')
                mention_amount(tweet,hashtag,comments_mention,index,index_2)
            elif search("(?i)invitez", tweet.full_text) :
                print('Mot clé trouvé, mention des amis...')
                mention_amount(tweet,hashtag,comments_mention,index,index_2)  
            elif search("(?i)tag",tweet.full_text) :
                print('Mot clé trouvé, mention des amis...')
                mention_amount(tweet,hashtag,comments_mention,index,index_2)
            elif search("(?i)identifie",tweet.full_text) :
                print('Mot clé trouvé, mention des amis...')
                mention_amount(tweet,hashtag,comments_mention,index,index_2)
            elif search("(?i)identifiez",tweet.full_text) :
                print('Mot clé trouvé, mention des amis...')
                mention_amount(tweet,hashtag,comments_mention,index,index_2)
            elif search("(?i)tague",tweet.full_text) :
                print('Mot clé trouvé, mention des amis...')
                mention_amount(tweet,hashtag,comments_mention,index,index_2)
            else :
                api.update_status('@'+tweet.user.screen_name+' '+hashtag+' '+comments[index_2],tweet.id)
                print('Commente le tweet, pas de mentions trouvées..')
    except TweepError as err :
        if err.api_code == 226 or err.api_code == 185 :
            print('Trop de requêtes, programme en stand by pendant 20 minutes')
            time.sleep(1250)
        elif err.api_code == 139 or err.api_code == 327 or err.api_code == 160 or err.response == 326 :
            pass
        else :
            print(err.reason)
        
def random_retweet() :
    """Retweet un tweet random"""
    try :
        #On récupère les hashtags en tendance à Paris 
        trends = api.trends_place(615702)
        #On en prend un au hasard qui n'est pas un concours
        random_trends = trends[0]['trends'][random.randint(0,len(trends[0]['trends'])-1)]['name']
        while random_trends == '#concours' or random_trends == '#Concours' :
            random_trends = trends[0]['trends'][random.randint(0,len(trends[0]['trends'])-1)]['name']
        #On recherche des tweets avec ce hashtag et on en retweet un
        for tweet in Cursor(api.search, q = random_trends, tweet_mode = 'extended', lang = 'fr', result_type = 'mixed').items(10) :
            #Si le tweet est un retweet
            if hasattr(tweet, 'retweeted_status') :
                #On vérifie que ce tweet n'est pas un concours
                if '#concours' not in tweet.retweeted_status.full_text or '#Concours' not in tweet.retweeted_status.full_text :
                    api.retweet(tweet.retweeted_status.id)
                    break
            #Si le tweet n'est pas un retweet
            else :
                #On vérifie que ce tweet n'est pas un concours
                if '#concours' not in tweet.full_text or '#Concours' not in tweet.full_text :
                    api.retweet(tweet.id)
                    break
    except TweepError as err :
        if err.api_code == 226 or err.api_code == 185 :
            print('Trop de requêtes, programme en stand by pendant 20 minutes')
            time.sleep(1250)
        elif err.api_code == 139 or err.api_code == 327 or err.api_code == 160 or err.response == 326 :
            pass
        else :
            print(err.reason)

def random_tweet() :
    """Génère un tweet aléatoire"""
    try :
        #On récupère les hashtags en tendance à Paris 
        trends = api.trends_place(615702)
        #On en prend un au hasard qui n'est pas un concours
        random_trends = trends[0]['trends'][random.randint(0,len(trends[0]['trends'])-1)]['name']
        while random_trends == '#concours' or random_trends == '#Concours' or random_trends == 'RT':
            random_trends = trends[0]['trends'][random.randint(0,len(trends[0]['trends'])-1)]['name']
        #On recherche des tweets avec ce hashtag et on en retweet un
        for tweet in Cursor(api.search, q = random_trends, tweet_mode = 'extended', lang = 'fr', result_type = 'mixed').items(10) :
            #Si le tweet est un retweet
            if hasattr(tweet, 'retweeted_status') :
                #On vérifie que ce tweet n'est pas un concours
                if '#concours' not in tweet.retweeted_status.full_text or '#Concours' not in tweet.retweeted_status.full_text or '#RT' not in tweet.retweeted_status.full_text or '#Follow' not in tweet.retweeted_status.full_text or 'Gagnez' not in tweet.retweeted_status.full_text :
                    api.update_status(tweet.retweeted_status.full_text.replace('@',''))        
                    break
            #Si le tweet n'est pas un retweet
            else :
                #On vérifie que ce tweet n'est pas un concours
                if '#concours' not in tweet.full_text or '#Concours' not in tweet.full_text :
                    api.update_status(tweet.full_text.replace('@',''))
                    break
    except TweepError as err :
        if err.api_code == 226 or err.api_code == 185 :
            print('Trop de requêtes, programme en stand by pendant 20 minutes')
            time.sleep(1250)
        elif err.api_code == 139 or err.api_code == 327 or err.api_code == 160 or err.response == 326 :
            pass
        else :
            print(err.reason)

def retweet_rate() :
    """Calcule le pourcentage de retweet sur un compte twitter"""
    try :
        nb_status = 0
        nb_retweeted_status = 0
        #On compte le nombre de tweets totaux et le nombre de retweet
        for status in api.user_timeline() :
            if status.retweeted :
                nb_status += 1
                nb_retweeted_status += 1
            else :
                nb_status += 1
        #On calcule le pourcentage
        if nb_retweeted_status > 0 :
            return (nb_retweeted_status / nb_status) *100
        else :
            return 0 
    except TweepError as err :
        if err.api_code == 226 or err.api_code == 185 :
            print('Trop de requêtes, programme en stand by pendant 20 minutes')
            time.sleep(1250)
        elif err.api_code == 139 or err.api_code == 327 or err.api_code == 160 or err.response == 326 :
            pass
        else :
            print(err.reason)

def retweet_concours_rate() :  
    """Calcule le pourcentage de concours auquel un compte twitter a participé"""
    try :
        nb_retweeted_status = 0
        nb_concours = 0
        for status in api.user_timeline(tweet_mode = 'extended') :
            #On calcule le nombre de retweet sur le compte twitter
            if status.retweeted :
                nb_retweeted_status += 1
                if '#concours' in status.retweeted_status.full_text or '#Concours' in status.retweeted_status.full_text or '#follow' in status.retweeted_status.full_text or '#Follow' in status.retweeted_status.full_text :
                    nb_concours += 1
        #On calcule le pourcentage de retweet  de concours par rapport au nombre de retweet totaux
        if nb_concours > 0 :
            return (nb_concours / nb_retweeted_status) *100
        else :
            return 0
    except  TweepError as err :
        if err.api_code == 226 or err.api_code == 185 :
            print('Trop de requêtes, programme en stand by pendant 20 minutes')
            time.sleep(1250)
        elif err.api_code == 139 or err.api_code == 327 or err.api_code == 160 or err.response == 326 :
            pass
        else :
            print(err.reason)          
def mention_amount(tweet,hashtag,comments_mention,index,index_2) :
    """Calcule le nombre d'amis à mentionner dans le tweet"""
    #Si le tweet est un retweet
    if hasattr(tweet,'retweeted_status') :
        split_text = tweet.retweeted_status.full_text.split()
        for word in split_text :
            #Regarde les 3 premières lettres de la string
            if word[:3] == 'ami' or word[:3] == 'Ami' or word[:3] == 'AMI':
                #Regarde le mot qui précède pour savoir combien d'amis il faut mentionner
                if split_text[split_text.index(word)-1] == 'un' or split_text[split_text.index(word)-1] == '1' or split_text[split_text.index(word)-1] == 'un(e)' :
                    api.update_status('@'+tweet.retweeted_status.author.screen_name+' '+hashtag+' '+comments_mention[index]+' @arthur6140 ',tweet.retweeted_status.id)
                elif split_text[split_text.index(word)-1] == 'deux' or split_text[split_text.index(word)-1] == '2' :
                    api.update_status('@'+tweet.retweeted_status.author.screen_name+' '+hashtag+' '+comments_mention[index]+' @arthur6140 @TheSalvio93 ',tweet.retweeted_status.id)
                elif split_text[split_text.index(word)-1] == 'trois' or split_text[split_text.index(word)-1] == '3' :
                    api.update_status('@'+tweet.retweeted_status.author.screen_name+' '+hashtag+' '+comments_mention[index]+' @arthur6140 @TheSalvio93 @_Nayyx',tweet.retweeted_status.id)
                elif split_text[split_text.index(word)-1] == 'quatre' or split_text[split_text.index(word)-1] == '4' :
                    api.update_status('@'+tweet.retweeted_status.author.screen_name+' '+hashtag+' '+comments_mention[index]+' @arthur6140 @TheSalvio93 @_Nayyx @Leeeeeper',tweet.retweeted_status.id)
            #Regarde les 8 premières lettres de la string
            if word[:8] == 'personne' or word[:8] == 'Personne' or word[:8] == 'PERSONNE' :
                #Regarde le mot qui précède pour savoir combien d'amis il faut mentionner
                if split_text[split_text.index(word)-1] == 'un' or split_text[split_text.index(word)-1] == '1' or split_text[split_text.index(word)-1] == 'un(e)' :
                    api.update_status('@'+tweet.retweeted_status.author.screen_name+' '+hashtag+' '+comments_mention[index]+' @arthur6140 ',tweet.retweeted_status.id)
                elif split_text[split_text.index(word)-1] == 'deux' or split_text[split_text.index(word)-1] == '2' :
                    api.update_status('@'+tweet.retweeted_status.author.screen_name+' '+hashtag+' '+comments_mention[index]+' @arthur6140 @TheSalvio93 ',tweet.retweeted_status.id)
                elif split_text[split_text.index(word)-1] == 'trois' or split_text[split_text.index(word)-1] == '3' :
                    api.update_status('@'+tweet.retweeted_status.author.screen_name+' '+hashtag+' '+comments_mention[index]+' @arthur6140 @TheSalvio93 @_Nayyx',tweet.retweeted_status.id)
                elif split_text[split_text.index(word)-1] == 'quatre' or split_text[split_text.index(word)-1] == '4' :
                    api.update_status('@'+tweet.retweeted_status.author.screen_name+' '+hashtag+' '+comments_mention[index]+' @arthur6140 @TheSalvio93 @_Nayyx @Leeeeeper',tweet.retweeted_status.id)

    #Si le tweet n'est pas un retweet
    else :
        split_text = tweet.full_text.split()
    for word in split_text :
        #Regarde les 3 premières lettres de la string
        if word[:3] == 'ami' or word[:3] == 'Ami' or word[:3] == 'AMI':
            #Regarde le mot qui précède pour savoir combien d'amis il faut mentionner
            if split_text[split_text.index(word)-1] == 'un' or split_text[split_text.index(word)-1] == '1' or split_text[split_text.index(word)-1] == 'un(e)' :
                api.update_status('@'+tweet.user.screen_name+' '+hashtag+' '+comments_mention[index]+' @arthur6140 ',tweet.id)
            elif split_text[split_text.index(word)-1] == 'deux' or split_text[split_text.index(word)-1] == '2' :
                api.update_status('@'+tweet.user.screen_name+' '+hashtag+' '+comments_mention[index]+' @arthur6140 @TheSalvio93 ',tweet.id)
            elif split_text[split_text.index(word)-1] == 'trois' or split_text[split_text.index(word)-1] == '3' :
                api.update_status('@'+tweet.user.screen_name+' '+hashtag+' '+comments_mention[index]+' @arthur6140 @TheSalvio93 @_Nayyx',tweet.id)
            elif split_text[split_text.index(word)-1] == 'quatre' or split_text[split_text.index(word)-1] == '4' :
                api.update_status('@'+tweet.user.screen_name+' '+hashtag+' '+comments_mention[index]+' @arthur6140 @TheSalvio93 @_Nayyx @Leeeeeper',tweet.id)
        #Regarde les 8 premières lettres de la string     
        if word[:8] == 'personne' or word[:8] == 'Personne' or word[:8] == 'PERSONNE' :
            #Regarde le mot qui précède pour savoir combien d'amis il faut mentionner
            if split_text[split_text.index(word)-1] == 'un' or split_text[split_text.index(word)-1] == '1' or split_text[split_text.index(word)-1] == 'un(e)' :
                api.update_status('@'+tweet.user.screen_name+' '+hashtag+' '+comments_mention[index]+' @arthur6140 ',tweet.id)
            elif split_text[split_text.index(word)-1] == 'deux' or split_text[split_text.index(word)-1] == '2' :
                api.update_status('@'+tweet.user.screen_name+' '+hashtag+' '+comments_mention[index]+' @arthur6140 @TheSalvio93 ',tweet.id)
            elif split_text[split_text.index(word)-1] == 'trois' or split_text[split_text.index(word)-1] == '3' :
                api.update_status('@'+tweet.user.screen_name+' '+hashtag+' '+comments_mention[index]+' @arthur6140 @TheSalvio93 @_Nayyx',tweet.id)
            elif split_text[split_text.index(word)-1] == 'quatre' or split_text[split_text.index(word)-1] == '4' :
                api.update_status('@'+tweet.user.screen_name+' '+hashtag+' '+comments_mention[index]+' @arthur6140 @TheSalvio93 @_Nayyx @Leeeeeper',tweet.id)

#Corps du programme

while True :
    participation(liste_recherche)
    waiting_time = random.randrange(2700, 3000)
    time.sleep(waiting_time)


