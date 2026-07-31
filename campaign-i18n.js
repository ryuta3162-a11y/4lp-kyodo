/**
 * キャンペーンLP — 言語切替時の動的文言・カルーセル
 */
(function () {
  function t(key, fallback) {
    return window.JoyfitI18n ? JoyfitI18n.t(key, fallback) : fallback;
  }

  function setText(id, key, fallback) {
    var el = document.getElementById(id);
    if (el) el.textContent = t(key, fallback);
  }

  function setHtml(id, key, fallback) {
    var el = document.getElementById(id);
    if (el) el.innerHTML = t(key, fallback);
  }

  function setAriaLabel(id, key, fallback) {
    var el = document.getElementById(id);
    if (el) el.setAttribute('aria-label', t(key, fallback));
  }

  var FREE_OPTIONS = [
    { id: 'hydrogen', icon_img: '37.png', amount: '3,240', ja: { name: '水素水 & プロテイン', description: '水素水＋プロテイン<br>[１日６杯迄]のお得なセット' } },
    { id: 'hotStudio', icon_img: '36.png', amount: '1,100', ja: { name: 'ホットスタジオ', description: '世田谷エリア最大級<br>のレッスンで滝汗体験!' } },
    { id: 'supportVip', icon_img: '41.png', amount: '825', ja: { name: 'あんしんサポートVIP', description: '万が一の時にも安心な<br>JOYFIT専用サポートプラン' } },
    { id: 'onlineLesson', icon_img: '42.png', amount: '1,100', ja: { name: 'オンラインレッスン', description: '自宅で本格的なレッスンが出来る!<br>ジムに来れない日でも安心' } },
    { id: 'tanning', icon_img: '44.png', amount: '5,500', ja: { name: 'タンニングマシン', description: '理想の日焼け肌を手に入れたい方へ!<br>※1日20分まで' } },
    { id: 'selfEsthe', icon_img: '45.png', amount: '3,300', ja: { name: 'セルフエステ', description: 'エステサロンと同じ<br>業務用マシンが使い放題' } },
    { id: 'rentalMat', icon_img: '38.png', amount: '1,100', ja: { name: 'レンタルマット', description: 'マットを持ってこなくてＯＫ!<br>ホットスタジオ参加には必須!' } },
    { id: 'rentalTowel', icon_img: '40.png', amount: '1,650', ja: { name: 'レンタルタオル', description: '汗をかいても安心レンタル<br>フェイスタオル・バスタオル' } },
    { id: 'bodyScale', icon_img: '39.png', amount: '550', ja: { name: '体組成計', description: '体脂肪、筋肉量を測定し<br>トレーニングを最適化' } }
  ];

  var PAID_OPTIONS = [
    { id: 'locker', icon_img: '43.png', amount: '1,650', ja: { name: '契約ロッカー', description: 'ウェアやシューズを置いたままに<br>あなた専用のロッカー' } },
    { id: 'pilates', icon_img: '46.png', amount: '3,300', ja: { name: 'ピラティスリフォーマー', description: 'ピラティスマシンを使い<br>体幹等を鍛える本格レッスン' } },
    { id: 'yogaLocker', icon_img: '47.png', amount: '1,100', ja: { name: 'ヨガマットロッカー', description: 'ご自身のヨガマットを保管<br>荷物を減らしたい方へ' } }
  ];

  var carouselState = { free: null, paid: null };

  function localizeOption(opt) {
    var base = 'options.items.' + opt.id;
    var isJa = !window.JoyfitI18n || JoyfitI18n.getLanguage() === 'ja';
    if (isJa) {
      return {
        name: opt.ja.name,
        description: opt.ja.description,
        amount: opt.amount,
        icon_img: opt.icon_img
      };
    }
    return {
      name: t(base + '.name', opt.ja.name),
      description: t(base + '.description', opt.ja.description),
      amount: opt.amount,
      icon_img: opt.icon_img
    };
  }

  function formatOptionPrice(amount) {
    if (!window.JoyfitI18n || JoyfitI18n.getLanguage() === 'ja') {
      return { main: amount + '円', sub: '月額', tax: '(税込)', style: 'ja' };
    }
    if (JoyfitI18n.getLanguage() === 'en') {
      return {
        main: '¥' + amount,
        sub: t('options.monthlyPrefix', 'Monthly'),
        tax: t('options.taxSuffix', '(tax incl.)'),
        style: 'en'
      };
    }
    return {
      main: amount + t('pricing.yen', '円'),
      sub: t('options.monthlyPrefix', '月額'),
      tax: t('options.taxSuffix', '(税込)'),
      style: 'cjk'
    };
  }

  function createCardHTML(option, isPaid) {
    var loc = localizeOption(option);
    var price = formatOptionPrice(loc.amount);
    var badge = isPaid
      ? t('options.paidBadge', '有料オプション')
      : t('options.freeBadge', '無料オプション');
    var priceHtml;
    if (price.style === 'en') {
      priceHtml = price.main + '<span style="font-size: 0.75rem; font-weight: normal; color: #555;"> / ' + price.sub + ' ' + price.tax + '</span>';
    } else {
      priceHtml = price.main + '<span style="font-size: 0.75rem; font-weight: normal; color: #555; font-family: \'Noto Sans JP\', sans-serif;"> / ' + price.sub + price.tax + '</span>';
    }
    return (
      '<div class="option-card-3d">' +
      '<div class="card-badge ' + (isPaid ? 'paid' : 'free') + '">' + badge + '</div>' +
      '<div style="width: 100%; flex-grow: 1; display: flex; justify-content: center; align-items: center; padding-bottom: 1rem;">' +
      '<img src="./' + loc.icon_img + '" alt="' + loc.name + '" class="card-icon" onerror="this.onerror=null; this.src=\'https://placehold.co/150x150/transparent/cccccc?text=Option\';">' +
      '</div>' +
      '<div style="width: 100%; flex-shrink: 0;">' +
      '<h4 class="card-title">' + loc.name + '</h4>' +
      '<p class="card-price font-impact text-xl" style="color: var(--brand);">' + priceHtml + '</p>' +
      '<p style="font-size: 0.75rem; color: #666; margin-top: 0.75rem; line-height: 1.5; min-height: 3.6rem;">' + loc.description + '</p>' +
      '</div></div>'
    );
  }

  function initializeCarousel(options, containerId, navPrevId, navNextId, isPaid) {
    var carouselContainer = document.getElementById(containerId);
    var prevBtn = document.getElementById(navPrevId);
    var nextBtn = document.getElementById(navNextId);
    if (!carouselContainer) return null;

    carouselContainer.innerHTML = options.map(function (opt) {
      return createCardHTML(opt, isPaid);
    }).join('');

    var cards = carouselContainer.querySelectorAll('.option-card-3d');
    var totalCards = cards.length;
    var currentIndex = 0;
    var autoPlayInterval = null;

    function updateCarousel() {
      var activeIndex = (currentIndex % totalCards + totalCards) % totalCards;
      cards.forEach(function (card, index) {
        var relativePos = ((index - activeIndex + totalCards) % totalCards);
        var transform = '';
        var opacity = 0;
        var zIndex = 0;
        switch (relativePos) {
          case 0: transform = 'translateX(-50%) scale(1)'; opacity = 1; zIndex = 20; break;
          case 1: transform = 'translateX(20%) scale(0.85)'; opacity = 0.6; zIndex = 10; break;
          case totalCards - 1: transform = 'translateX(-120%) scale(0.85)'; opacity = 0.6; zIndex = 10; break;
          default:
            transform = relativePos < totalCards / 2 ? 'translateX(50%) scale(0.6)' : 'translateX(-150%) scale(0.6)';
            opacity = 0;
            zIndex = 0;
            break;
        }
        card.style.transform = transform;
        card.style.opacity = opacity;
        card.style.zIndex = zIndex;
      });
    }

    function startAutoPlay() {
      if (autoPlayInterval) clearInterval(autoPlayInterval);
      autoPlayInterval = setInterval(function () {
        currentIndex++;
        updateCarousel();
      }, 4000);
    }

    function stopAutoPlay() {
      if (autoPlayInterval) {
        clearInterval(autoPlayInterval);
        autoPlayInterval = null;
      }
    }

    if (prevBtn) {
      prevBtn.onclick = function () {
        currentIndex--;
        updateCarousel();
        stopAutoPlay();
        startAutoPlay();
      };
    }
    if (nextBtn) {
      nextBtn.onclick = function () {
        currentIndex++;
        updateCarousel();
        stopAutoPlay();
        startAutoPlay();
      };
    }

    var startX = 0;
    var isDragging = false;
    carouselContainer.ontouchstart = function (e) {
      startX = e.touches[0].clientX;
      isDragging = true;
      stopAutoPlay();
    };
    carouselContainer.ontouchend = function (e) {
      if (!isDragging) return;
      var diff = startX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 50) {
        if (diff > 0) currentIndex++;
        else currentIndex--;
        updateCarousel();
      }
      isDragging = false;
      startAutoPlay();
    };

    updateCarousel();
    startAutoPlay();

    return { stop: stopAutoPlay };
  }

  function initCarousels() {
    if (carouselState.free && carouselState.free.stop) carouselState.free.stop();
    if (carouselState.paid && carouselState.paid.stop) carouselState.paid.stop();
    carouselState.free = initializeCarousel(FREE_OPTIONS, 'card-carousel-free', 'carousel-prev-free', 'carousel-next-free', false);
    carouselState.paid = initializeCarousel(PAID_OPTIONS, 'card-carousel-paid', 'carousel-prev-paid', 'carousel-next-paid', true);
  }

  function applyCampaignDynamic() {
    setText('campaign-option-label', 'pricing.optionLabel', '8月オプション');
    setText('campaign-option-label-sub', 'pricing.optionLabelSub', '無料オプション8つ自動契約');
    setText('campaign-option-highlight', 'pricing.optionHighlight', '8月分が0円');
    setHtml(
      'campaign-option-note',
      'pricing.optionNote',
      '※8つのオプションは入会時自動契約されます。<br>不要な場合は<span id="campaign-option-cancel-deadline">8月末</span>までに解約をお願いいたします。'
    );
    setText('campaign-option-cancel-deadline', 'pricing.optionCancelDeadline', '8月末');
    setText('campaign-notice-deadline', 'pricing.noticeDeadline', '8月末迄');

    if (window.JoyfitI18n && JoyfitI18n.getLanguage() !== 'ja') {
      setText('dynamic-date-label', 'pricing.joinAmountLabel', 'ご入会時金額');
    }

    setAriaLabel('carousel-prev-free', 'options.prevFree', '前の無料オプション');
    setAriaLabel('carousel-next-free', 'options.nextFree', '次の無料オプション');
    setAriaLabel('carousel-prev-paid', 'options.prevPaid', '前の有料オプション');
    setAriaLabel('carousel-next-paid', 'options.nextPaid', '次の有料オプション');

    if (typeof window.updateProratedFee === 'function') {
      window.updateProratedFee();
    }

    initCarousels();
  }

  document.addEventListener('DOMContentLoaded', function () {
    if (window.JoyfitI18n && JoyfitI18n.getLanguage) {
      applyCampaignDynamic();
    }
  });
  window.addEventListener('joyfit:langchange', applyCampaignDynamic);

  window.CampaignI18n = { apply: applyCampaignDynamic, initCarousels: initCarousels };
})();
