
#these are the even messages that we can change and use how we like
async def send_message(message, user_message, is_private):
    try:
        response = handle_response(user_message)
        await message.author.send(
            response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

def handle_response(message) -> str:
    p_message = message.lower()
  
    if p_message == 'hello':
        return 'Hey there!'

    if p_message == '!gamehours':
      return 'The game room hours are from 10am Monday  through Friday \nBUT sometimes our teams will be practicing on cerain Mondays,Tuesdays, Fridays and if they are, the Game Room would start wrapping up around 5:30 to prep for our teams from 6-8pm'

    if p_message == '!help':
        return 'commands include \n!gamehours\n!location\n!hello'
      
    if p_message == '!location':
        return 'The USU Games Room is located in the lower level of the East Conference Center, across from the Student Recreation Center. \nFor more information visit the website \nhttps://www.csun.edu/src/games-room%27%27'