import json
from django.views.generic.base import TemplateView
from utils.nfts_redis import get_nfts_from_redis
from utils.wallet_info import get_nexid_nft_balance, get_nexid_nft_price, get_nexid_token_balance


class IndexTemplateView(TemplateView):
    """
    Render the homepage template.
    """

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)

        values = get_nfts_from_redis()
        nfts = []
        if values is not None:
            for value in values:
                nfts.append(json.loads(value))
        context['nfts'] = nfts
        context['nexid_token_balance'] = get_nexid_token_balance()
        context['nexid_nft_balance'] = get_nexid_nft_balance()
        context['nexid_nft_price'] = get_nexid_nft_price()

        return context
