from aiogram.utils.markdown import hbold

from database.models import Product


def get_answer(product: Product) -> str:
	answer = f"{hbold(product.title)}\n\n" \
			 f"артикул: {product.article}\n" \
			 f"цена: {product.price}р.\n" \
			 f"рейтинг: {product.rate}\n" \
			 f"количество на складах: {product.quantity}\n" \
			 f"данные актуальны на {product.date}\n"
	return answer