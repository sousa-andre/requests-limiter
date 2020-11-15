# requests-limiter
##### Rate limiting made easy.

![PyPi badge](https://img.shields.io/pypi/v/requests-limiter?style=for-the-badge) ![Code size badge](https://img.shields.io/github/languages/code-size/sousa-andre/requests-limiter?style=for-the-badge) ![License badge](https://img.shields.io/github/license/sousa-andre/requests-limiter?style=for-the-badge)
 
Have fun using third-parties REST APIs without have to worry about rate limiting. 
 
## Download
    $ pip install requests-limiter 

## Example
Take a look into the [example](examples/riotapi) that creates a simple rate limiter for the Riot API [SummonerV4](https://developer.riotgames.com/apis#summoner-v4) endpoints.

## To-do
   - Make the library thread-safe
   - Write the logic in C/C++ in order to support more languages with the same codebase
   - Create a utility module
