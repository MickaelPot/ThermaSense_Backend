DISPOSE_LORA = False

def demandeTemperature():
    if not DISPOSE_LORA:
        #si vous ne disposez pas de recepteur LORA, le programme genere une temperature au hasard
        import random
        temperature_minimale = 15
        temperature_maximale = 26
        #Génére un entier aléatoire entre les temperatures spécifiées
        temperature_aleatoire = random.randint(temperature_minimale, temperature_maximale)
        return temperature_aleatoire
    from random import randint
    from time import time
    from rak811.rak811_v3 import Rak811
    P2P_BASE = 30
    P2P_RANDOM = 60

    lora = Rak811()

    print('Configuration du module de reception')
    response = lora.set_config('lora:work_mode:1')
    for r in response:
        print(r)
  
    freq = 869.800
    sf = 7
    bw = 0  # 125KHz
    ci = 1  # 4/5
    pre = 8
    pwr = 16
    lora.set_config(f'lorap2p:{int(freq*1000*1000)}:{sf}:{bw}:{ci}:{pre}:{pwr}')

    data=""
    try:
        while True:
            time_out = time() + P2P_BASE + randint(0, P2P_RANDOM)
            lora.set_config('lorap2p:transfer_mode:1')
            wait_time = time_out - time()
            lora.receive_p2p(wait_time)
            while lora.nb_downlinks > 0:
                message = lora.get_downlink()
                data = message['data']
                data = data.decode('utf-8')
                break
            break
    except:  # noqa: E722
        pass
    print('Recuperation des données terminées')
    return data