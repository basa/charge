# -*- coding: utf-8 -*-

# Taken from:
#     https://github.com/titusz/py-moneyed/blob/master/src/moneyed/converter.py

# Copyright (c) 2011 Kai Wu, k@limist.com
# All rights reserved.
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:   
# * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# * Neither the names of the copyright holders of this software, nor its contributors, may be used to endorse or promote products derived from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import urllib2
from moneyed.classes import Currency, Money
from decimal import Decimal


class ConversionRates(object):
    URL = 'http://finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s={from_curr}{to_curr}=X'

    def __init__(self):
        self._rates = {}

    def get(self, from_curr, to_curr):
        """Get conversion rate from session cache or get current from yahoo"""
        if isinstance(from_curr, Currency):
            from_curr = from_curr.code
        if isinstance(to_curr, Currency):
            to_curr = to_curr.code
        if not self._rates.get(from_curr + to_curr):
            fx_rate = self._get_rate(from_curr, to_curr)
            self._rates[from_curr + to_curr] = fx_rate
            return fx_rate
        else:
            return self._rates.get(from_curr + to_curr)

    def _get_rate(self, from_curr, to_curr='USD'):
        if from_curr.lower() == to_curr.lower():
            return Decimal('1.0')
        data = self._get_data(self.URL.format(from_curr=from_curr,
                                              to_curr=to_curr))
        if data:
            exchange = data.split(',')
            return Decimal(exchange[1])

    def _get_data(self, url):
        request = urllib2.Request(url, None, {'Accept-encoding': '*'})
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError:
            return None
        result = response.read()
        return result


CONVERSION_RATES = ConversionRates()

def convert(money, to_currency):
    fx_rate = CONVERSION_RATES.get(money.currency.code, to_currency)
    return Money(money.amount * fx_rate, to_currency)
