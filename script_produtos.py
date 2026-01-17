import os
import django
from decimal import Decimal

# 🔥 AJUSTE AQUI PARA O NOME DO SEU PROJETO
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "project.settings"  # <<< nome da pasta do projeto
)

django.setup()

# agora pode importar models
from product.models import Product, Category, Promotion

# ===============================
# SCRIPT DE CADASTRO EM MASSA
# ===============================

category, _ = Category.objects.get_or_create(category="Tênis")

promotion = Promotion.objects.filter(name="Promo Verão").first()

from decimal import Decimal

products = [
    {
        "name": "Samba OG",
        "category": "Calçados",
        "description": "Nascido nos campos de futebol, o Samba é um ícone atemporal do estilo street. Possui cabedal em couro macio, camurça granulada e a clássica sola de borracha natural que oferece excelente tração e durabilidade.",
        "price": Decimal("599.99"),
    },
    {
        "name": "Ultraboost 1.0",
        "category": "Calçados",
        "description": "Desenvolvido para máximo desempenho e conforto, este tênis utiliza a tecnologia Boost de retorno de energia e o cabedal Primeknit que se ajusta ao pé como uma meia, ideal para corridas e uso diário intenso.",
        "price": Decimal("1199.99"),
    },
    {
        "name": "Gazelle Indoor",
        "category": "Calçados",
        "description": "Um clássico relançado com detalhes premium. Este tênis apresenta cabedal em camurça de alta qualidade e o icônico solado de borracha translúcida, mantendo o visual vintage que conquistou as arquibancadas nos anos 70.",
        "price": Decimal("699.90"),
    },
    {
        "name": "Calça Legging Techfit",
        "category": "Calças",
        "description": "Projetada para treinos de alta intensidade, esta legging oferece compressão muscular para reduzir a fadiga. Conta com tecnologia AEROREADY para absorção de suor e cintura alta para suporte garantido durante movimentos bruscos.",
        "price": Decimal("259.90"),
    },
    {
        "name": "Shorts Mesh Essentials",
        "category": "Shorts",
        "description": "Leve e respirável, este shorts é confeccionado em malha de poliéster reciclado. Possui painéis laterais que favorecem a ventilação e cós elástico com cordão, sendo a escolha perfeita para basquete ou treinos de perna.",
        "price": Decimal("149.90"),
    },
    {
        "name": "Bolsa Duffel Essentials Logo",
        "category": "Bolsas",
        "description": "Espaçosa e funcional, esta mala de academia possui compartimento isolado para calçados sujos e bolsos internos para organização. O material é reforçado na base para suportar o atrito com o chão e o uso frequente.",
        "price": Decimal("229.90"),
    },
    {
        "name": "Adizero Adios Pro 3",
        "category": "Calçados",
        "description": "O tênis de competição definitivo para maratonistas. Equipado com as EnergyRods de carbono que limitam a perda de energia e duas camadas de espuma Lightstrike Pro para o amortecimento mais responsivo da categoria.",
        "price": Decimal("1899.90"),
    },
    {
        "name": "Calça Treino Tiro 23",
        "category": "Calças",
        "description": "Um clássico do futebol adaptado para o dia a dia. Possui corte afunilado para não atrapalhar o contato com a bola, zíperes nos tornozelos para facilitar o vestir e tecido antissuor de secagem rápida.",
        "price": Decimal("349.90"),
    },
    {
        "name": "Shorts Running Own The Run",
        "category": "Shorts",
        "description": "Shorts de corrida focado em performance noturna, com detalhes refletivos em 360 graus. Inclui cueca interna integrada para suporte extra e bolso à prova de suor para proteger seus dispositivos eletrônicos.",
        "price": Decimal("199.90"),
    },
    {
        "name": "Mochila Power VI",
        "category": "Bolsas",
        "description": "Construída para o ritmo escolar e profissional, conta com divisória acolchoada para notebook e alças com tecnologia Loadspring que absorvem o impacto do peso nos ombros durante o transporte.",
        "price": Decimal("299.90"),
    },
    {
        "name": "Stan Smith Primegreen",
        "category": "Calçados",
        "description": "O design clássico que nunca sai de moda, agora atualizado com materiais sustentáveis de alto desempenho. Visual limpo com as Três Listras perfuradas e o icônico detalhe verde no calcanhar com a assinatura do tenista.",
        "price": Decimal("499.90"),
    },
    {
        "name": "Calça Pantalona Adicolor",
        "category": "Calças",
        "description": "Estilo retrô e volumoso com as três listras laterais. Esta calça pantalona oferece conforto extremo com tecido de malha premium, ideal para compor looks urbanos modernos e despojados.",
        "price": Decimal("449.90"),
    },
    {
        "name": "Shorts de Banho 3-Stripes",
        "category": "Shorts",
        "description": "Desenvolvido para atividades aquáticas e lazer, este shorts é feito de tecido leve de secagem ultrarrápida. Possui calção interno em mesh e bolsos laterais para praticidade fora da água.",
        "price": Decimal("179.90"),
    },
    {
        "name": "Mochila Adventure Top Loader",
        "category": "Bolsas",
        "description": "Inspirada em equipamentos de escalada vintage, esta mochila possui abertura superior por cordão e fivelas de engate rápido. Feita em tecido ripstop ultra resistente para trilhas urbanas ou natureza.",
        "price": Decimal("549.90"),
    },
    {
        "name": "Predator Elite FG",
        "category": "Calçados",
        "description": "Chuteira profissional para gramado natural firme. Apresenta elementos de borracha Strikeskin posicionados estrategicamente para máximo controle de bola e precisão absoluta em chutes de longa distância.",
        "price": Decimal("1999.99"),
    },
    {
        "name": "Calça Jogger Essentials French Terry",
        "category": "Calças",
        "description": "Feita com uma mistura de algodão e poliéster reciclado, esta jogger oferece o toque macio do moletom por dentro. Barra elástica ajustada e visual minimalista para momentos de descanso ou lazer.",
        "price": Decimal("279.90"),
    },
    {
        "name": "Shorts Farm Rio Print",
        "category": "Shorts",
        "description": "Colaboração exclusiva com a Farm Rio, trazendo cores vibrantes e estampas tropicais. O corte solto permite liberdade de movimento total, unindo o DNA esportivo da Adidas ao estilo brasileiro.",
        "price": Decimal("229.90"),
    },
    {
        "name": "Pochete Adicolor Classic",
        "category": "Bolsas",
        "description": "Compacta e estilosa, esta pochete permite carregar itens essenciais com segurança. Possui dois compartimentos com zíper e cinto ajustável, podendo ser usada na cintura ou atravessada no peito.",
        "price": Decimal("129.90"),
    },
    {
        "name": "NMD_R1 V3",
        "category": "Calçados",
        "description": "A evolução do clássico NMD, apresentando detalhes táticos e plugues na entressola de visual futurista. O amortecimento Boost garante que cada passo seja suave, independentemente da distância percorrida na cidade.",
        "price": Decimal("999.90"),
    },
    {
        "name": "Calça Terrex Zupahike",
        "category": "Calças",
        "description": "Calça técnica de trilha com design híbrido. Painéis frontais resistentes ao clima combinam com painéis traseiros respiráveis, permitindo agilidade e proteção em terrenos rochosos e encostas íngremes.",
        "price": Decimal("799.90"),
    },
    {
        "name": "Shorts Yoga Studio Base",
        "category": "Shorts",
        "description": "Desenvolvido especificamente para a prática de Yoga e Pilates, possui tecido macio que não limita o movimento. Costuras planas reduzem o atrito com a pele durante as posturas mais complexas.",
        "price": Decimal("189.90"),
    },
    {
        "name": "Mala de Viagem Trolley",
        "category": "Bolsas",
        "description": "Equipada com rodas suaves e alça telescópica, esta mala é ideal para viagens curtas de atletas. Construção em lona resistente e diversos bolsos organizadores para documentos e eletrônicos.",
        "price": Decimal("899.90"),
    },
    {
        "name": "Superstar XLG",
        "category": "Calçados",
        "description": "Uma versão ousada do clássico com biqueira shell toe. O modelo XLG apresenta uma entressola plataforma elevada e detalhes ampliados para quem busca destaque visual sem abrir mão da herança histórica.",
        "price": Decimal("649.90"),
    },
    {
        "name": "Calça Cargo Streetwear",
        "category": "Calças",
        "description": "Estética utilitária com bolsos laterais grandes. Feita em sarja de algodão durável, esta calça oferece um caimento relaxado que combina perfeitamente com tênis robustos e camisetas oversized.",
        "price": Decimal("529.90"),
    },
    {
        "name": "Shorts 2 em 1 HIIT",
        "category": "Shorts",
        "description": "Combina um shorts externo leve com uma bermuda de compressão interna. Evita assaduras e oferece cobertura total durante agachamentos e saltos em treinos funcionais de alta intensidade.",
        "price": Decimal("249.90"),
    },
    {
        "name": "Bolsa Tote Originals",
        "category": "Bolsas",
        "description": "Uma bolsa de ombro versátil para o dia a dia. Possui fechamento em zíper e alças reforçadas, perfeita para carregar compras casuais ou equipamentos leves de treino com um toque de elegância.",
        "price": Decimal("199.90"),
    },
    {
        "name": "Forum Low Classic",
        "category": "Calçados",
        "description": "Originalmente um tênis de basquete, o Forum Low mantém sua icônica tira de velcro no tornozelo e construção em camadas. Um símbolo de status cultural que oferece conforto e suporte lateral superior.",
        "price": Decimal("649.90"),
    },
    {
        "name": "Calça Firebird Track Pant",
        "category": "Calças",
        "description": "A calça de agasalho definitiva. Feita com o brilho clássico do tricô de poliéster reciclado, apresenta as três listras bordadas e zíper na barra, mantendo a autenticidade da linha Adicolor.",
        "price": Decimal("379.90"),
    },
    {
        "name": "Shorts Club Tennis",
        "category": "Shorts",
        "description": "Otimizado para as quadras de saibro e rápida, este shorts possui tecnologia AEROREADY e bolsos fundos projetados especificamente para armazenar bolinhas de tênis com segurança durante o jogo.",
        "price": Decimal("169.90"),
    },
    {
        "name": "Bolsa Organizadora Festival",
        "category": "Bolsas",
        "description": "Pequena e prática, ideal para shows e eventos. Cabe exatamente o celular, carteira e chaves. Possui alça ajustável removível, permitindo o uso como necessaire dentro de mochilas maiores.",
        "price": Decimal("119.90"),
    }
]

for p in products:
    Product.objects.create(
        name=p["name"],
        category=category,
        description=p["description"],
        price=p["price"],
        discount=promotion
    )

print("✅ Produtos cadastrados com sucesso!")
