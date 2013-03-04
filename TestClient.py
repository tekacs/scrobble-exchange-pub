# Import thrift stuff
from se_api import ScrobbleExchange
from se_api.ttypes import *
from se_api.constants import *
from thrift import Thrift
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
# End of thrift

#ec2-54-246-25-244.eu-west-1.compute.amazonaws.com
API_SERVER = 'ec2-54-246-25-244.eu-west-1.compute.amazonaws.com'
API_PORT = 9090

authed = AuthUser(money=None, session_key=u'1a4602d8af05a8330611ff408b3edbdf', 
newuser=False, name=User(profileimage=None, points=None, name=u'Sov1etRuss1a'))

unauthunames = ['simonmoran', 'foreverautumn', 'theneonfever', 'robinlisle',
                'nancyvw', 'miadellocca', 'massdosage', 'mbrodbelt',
                'hyperchris01', 'ben-xo', 'gamboviol', 'good_bone', 'caitlin',
                'francescatanner', 'Knapster01', 'eartle', 'teabot', 'jorge',
                'colins', 'sjransome', 'Maddieman', 'wsbk', 'darkspark88',
                'grahamtodman', 'y0b1tch', 'monkeyhacker', 'FofR', 'Pbad',
                'pellitero', 'dasistdasende', 'Thomas_prince', 'sven',
                'CarbonParlour', 'phuedx', 'tdhooper', 'pduin', 'ssk2',
                'marekventur', 'jammus', 'dodgyfox', 'okspud1']

alist = ['coldplay', 'rot', 'denver', 'rihanna',
        'rin toshite shigure', '\u51db\u3068\u3057\u3066\u6642\u96e8',
        'brosef', 'radiohead', 'mumford & sons']

try:
    # Connect to the API server
    transport = TSocket.TSocket(API_SERVER, API_PORT)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = ScrobbleExchange.Client(protocol)
    transport.open()
    # End
    
    #Test the apikey
    print 'Testing apikey()'
    print client.apikey()
    
    ##Testing the login function
    #print '\nTesting login(token: string)'
    #slist = ['3084916df7ed2ae457be656facf5a9c0']
    #for s in slist:
        #try:
            #print client.login(s)
        #except AuthenticationError:
            #print s + ' was not accepted as an argument'
    
    ##Testing the getArtist function
    #print '\nTesting getArtist(artist: Artist)'
    #try:
        #for s in alist:
            #a = Artist(mbid='', name=s)
            #print s
            #print client.getArtist(a)
            
        ##sending false mbids used to lead to errors
        #a = Artist(mbid='trolol')
        #print client.getArtist(a)
        #a = Artist(mbid='',name='')
        #print client.getArtist(a)
    #except:
        #pass
   
    ##Testing the getLightArtist function
    ##Essentially the above but returns less, so same edge cases
    #print '\nTesting getLightArtist(artist: Artist)'
    #for s in alist:
        #try:
            #a = Artist(mbid='', name=s)
            #print client.getLightArtist(a)
        #except:
            #pass
    
    #Testing the getArtistSE function
    print '\nTesting getArtistSE(artist: Artist, user: User)'  
    for u in unauthunames:
        try:
            a = Artist(mbid='', name='coldplay')
            user = User(name=u)
            print client.getArtistSE(a,user)
        except:
            pass
            
    ##Testing the getArtistLFM function
    #print '\nTesting getArtistLFM(artist: Artist, user: User)'
    #for s in alist:
        #try:
            #a = Artist(mbid='', name=s)
            #print client.getArtistLFM(a)
        #except:
            #pass
    
    ##Testing the getArtistHistory function
    #print '\nTesting getArtistHistory(artist: Artist, n: int)'
    #for s in alist:
        #try:
            #a = Artist(mbid='', name=s)
            #print client.getArtistHistory(a,5)
        #except:
            #pass
    
    ##Testing the searchArtist function
    #print '\nTesting searchArtist(text:string, n: int, page: int)'
    #tlist = ['coldplay','coldp','brose','&','rin toshite',' ']
    #for t in tlist:
        #try:
            #print client.searchArtist(t,5,1)
        #except:
            #pass
    
    ##Testing the getSETop function
    #print '\nTesting getSETop(n: int, trange:int)'
    #try:
        #u = User('')
        #print client.getSETop(5,5,u)
    #except:
        #pass
    
    ##Testing the getLFMTop function
    #print '\nTesting getLFMTop(n: int)'
    #try:
        #u = User('')
        #print client.getLFMTop(5,u)
    #except:
        #pass
        
    ##Testing the getTradedArtists function
    ##TODO: as yet this is not done
    #print '\nTesting getTradedArtists(n: int)'
    #try:
        #print client.getTradedArtists(5)
    #except:
        #pass
    
    ##Testing the getRecentTrades function
    #print '\nTesting getRecentTrades(n: int)'
    #try:
        #print client.getRecenTrades(5)
    #except:
        #pass
      
    ##Testing the getUserData function
    #print '\nTesting getUserData(user: string)'
    #for u in unauthunames:
        #try:
            #print client.getUserData(u)
        #except:
            #pass
    
    ##Testing the getUserMoney function
    #print '\nTesting getUserMoney(user: AuthUser)'
    #try:
        #print client.getUserMoney(authed)
    #except:
        #pass
    
    ##Testing the getLeagues function
    #print '\nTesting getLeagues()'
    #try:
        #print client.getLeagues()
    #except:
        #pass
    
    ##Testing the getTopUsers function
    ##TODO: doesn't include leagues
    #print '\nTesting getTopUsers(n: int, league: League, trange: int)'
    #try:
        #print client.getTopUsers(5, League(uid='bronze'), 20)
    #except:
        #pass
        
    ##Testing the getNearUsers function
    ##TODO: User doesn't have an attribute near
    #print '\nTesting getNearUsers(user: string)'
    #for u in ulist:
        #try:
            #print client.getNearUsers(u)
        #except:
            #pass
    
    ##Testing the getGuarantee function
    #print '\nTesting getGuarantee(artist: Artist, user: AuthUser)'
    
    #a = Artist(mbid='',name='coldplay')
   
    #guaran = client.getGuarantee(a,authed)
    #print guaran
    
    ##Testing the buy function
    #print '\nTesting buy(guarantee: Guarantee, user: AuthUser)'
    #print client.buy(guaran,authed)
    
    ##Testing the sell function
    #print '\nTesting sell(guarantee: Guarantee, user: AuthUser)'
    #print client.sell(guaran,authed)
    
    
except Thrift.TException, tx:
    print '%s' % (tx.message)
