import pyttsx3
import time 

engine = pyttsx3.init()
voices = engine.getProperty("voices")

        
    
engine.setProperty("voice", voices[11].id)
print("====SPEAKING====")
newVoiceRate = 170
engine.setProperty("rate", newVoiceRate)
text="""What happened.The market rout that drove the value of nearly all risk assets lower on Tuesday appears to have paused for stocks on Wednesday, but it's continuing in the world of cryptocurrencies. The Bureau of Labor Statistics delivered its August consumer price index report Tuesday, and the inflation rate clocked in at a higher-than-expected 8.3% year over year. That was lower than July's 8.5 result, but it still hit most major tokens hard. Continued selling pressure has resulted in declines in top tokens Bitcoin (BTC -1.81) and Solana (SOL -2.36%) of 3.5% and 4.1%, respectively, over the past 24 hours, as of 11:15 a.m. ET Wednesday...For investors in Terra Luna Classic (LUNC -16.54%), some disheartening token-specific news has driven a 21.6% decline over this same period. On Wednesday, a South Korean court issued arrest warrants  for Terraform Labs founder Do Kwon and five other involved individuals. It may be the last nail in the coffin for this embattled project, which had previously seen speculative buying pressure from traders...So what.Nearly all talk about the potential for low-beta exposure to risk assets via cryptocurrencies is over. There has been an impressive degree of correlation between digital assets and equities over the past two years, which has been very unfavorable to crypto investors during this year's sell-off. While this correlation has diminished from its all-time peak, generally speaking, the same macroeconomic forces that drive equities higher or lower appear to have significant influence over the price action of many top tokens..Bitcoin and Solana are both attracting a significant amount of institutional investor interest. Accordingly, during this period of de-risking, these assets could continue to see outflows until the rhetoric around monetary policy shifts. In general, more expensive money means less liquidity searching for growth. For these high-upside, higher-risk assets, that could spell continued downward pressure, at least over the near term..For investors in Terra's ecosystem of tokens, word that arrest warrants have been issued is probably the last thing they wanted to hear. Whether one is involved in LUNC or other Terra-related assets, the advance of the regulatory probe to this degree is just the latest in a barrage of negative catalysts. Investors have reason to be concerned about the viability of the Terra ecosystem following this news, particularly given the turmoil within the Terra community... .....Now what.Whether investors are considering quality crypto projects or more speculative options, it's a tough time to be an investor right now. Macro headwinds abound, providing a bearish backdrop for all digital assets. And when it comes to those with token-specific issues such as LUNC, now does not seem like the time to throw good money after bad..."""
engine.save_to_file(text.replace("%","").replace(". ","").replace("-"," ").replace(","," ").lower().strip(), f"fiverr/test.mp3")


engine.runAndWait()

