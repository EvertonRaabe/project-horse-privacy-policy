# admob.py
from config import ADMOB_REWARDED_ID
import sys as _sys

_IS_ANDROID = not _sys.platform.startswith('linux') or 'ANDROID_ARGUMENT' in __import__('os').environ

if not _IS_ANDROID:
    # ── Stub para desktop ─────────────────────────────────────────────────────
    def inicializar():
        print("[AdMob] Stub: fora do Android — ignorado")

    def anuncio_disponivel():
        return False

    def exibir_anuncio(callback=None):
        print("[AdMob] Stub: sem anúncio no desktop")
        return False

else:
    from jnius import autoclass, PythonJavaClass, java_method
    from kivy.clock import Clock

    # ── Configuração AdMob ────────────────────────────────────────────────────
    MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
    AdRequestBuilder = autoclass('com.google.android.gms.ads.AdRequest$Builder')
    RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
    RewardedAdLoadCallback = autoclass('com.google.android.gms.ads.rewarded.RewardedAdLoadCallback')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')

    _activity = PythonActivity.mActivity
    ADMOB_ID = ADMOB_REWARDED_ID  # Pega do config.py
    _rewarded_ad = None
    _reward_callback = None

    # ── Callbacks ─────────────────────────────────────────────────────────────
    class MyRewardedAdLoadCallback(RewardedAdLoadCallback):
        def __init__(self):
            super().__init__()
        
        @java_method('(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V')
        def onRewardedAdLoaded(self, ad):
            global _rewarded_ad
            _rewarded_ad = ad
            print("[AdMob] ✅ Anúncio carregado!")
        
        @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
        def onRewardedAdFailedToLoad(self, error):
            print(f"[AdMob] ❌ Falha ao carregar: {error}")

    class MyRewardedAdCallback(RewardedAdLoadCallback):
        def __init__(self, callback):
            global _reward_callback
            super().__init__()
            _reward_callback = callback
        
        @java_method('()V')
        def onUserEarnedReward(self, reward):
            print(f"[AdMob] 🎁 Recompensa: {reward.getAmount()} {reward.getType()}")
            if _reward_callback:
                _reward_callback()
        
        @java_method('()V')
        def onRewardedAdClosed(self):
            print("[AdMob] 🔒 Anúncio fechado")
            carregar_anuncio()
        
        @java_method('()V')
        def onRewardedAdOpened(self):
            print("[AdMob] 👁️ Anúncio aberto")
        
        @java_method('()V')
        def onRewardedAdFailedToShow(self, error):
            print(f"[AdMob] ❌ Falha ao mostrar: {error}")

    # ── Funções públicas ──────────────────────────────────────────────────────
    def inicializar():
        MobileAds.initialize(_activity)
        print("[AdMob] 🚀 Inicializado")
        carregar_anuncio()

    def carregar_anuncio():
        global _rewarded_ad
        print("[AdMob] 📡 Carregando anúncio...")
        builder = AdRequestBuilder()
        request = builder.build()
        load_callback = MyRewardedAdLoadCallback()
        try:
            RewardedAd.load(_activity, ADMOB_ID, request, load_callback)
        except Exception as e:
            print(f"[AdMob] ERRO: {e}")

    def exibir_anuncio(callback=None):
        global _rewarded_ad
        if _rewarded_ad is not None:
            print("[AdMob] ▶️ Mostrando anúncio...")
            ad_callback = MyRewardedAdCallback(callback)
            _rewarded_ad.show(_activity, ad_callback)
            return True
        else:
            print("[AdMob] ⚠️ Anúncio não pronto")
            carregar_anuncio()
            return False

    def anuncio_disponivel():
        return _rewarded_ad is not None
