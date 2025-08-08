"""add_test_data"""

from alembic import op

# revision identifiers
revision = 'add_test_data'
down_revision = 'create_tables'
branch_labels = None
depends_on = None


def upgrade():
    # Здания
    op.execute("""
    INSERT INTO buildings (id, address, latitude, longitude) VALUES
    (1, 'г. Москва, ул. Ленина 1, офис 3', 55.7558, 37.6173),
    (2, 'г. Москва, ул. Блюхера 32/1', 55.7625, 37.6163),
    (3, 'г. Санкт-Петербург, Невский пр. 28', 59.9343, 30.3351),
    (4, 'г. Казань, ул. Баумана 15', 55.7964, 49.1088),
    (5, 'г. Сочи, ул. Навагинская 9', 43.5855, 39.7231)
    """)

    # Виды деятельности (3 уровня)
    op.execute("""
    INSERT INTO activities (id, name, category, parent_id, level) VALUES
    -- 1 уровень (корневые)
    (1, 'Еда', 'food', NULL, 1),
    (2, 'Автомобили', 'auto', NULL, 1),
    (3, 'Услуги', 'services', NULL, 1),
    (4, 'Строительство', 'construction', NULL, 1),
    
    -- 2 уровень (подкатегории)
    -- Для "Еды"
    (5, 'Мясная продукция', 'meat', 1, 2),
    (6, 'Молочная продукция', 'dairy', 1, 2),
    (7, 'Овощи и фрукты', 'vegetables', 1, 2),
    
    -- Для "Автомобилей"
    (8, 'Грузовые', 'trucks', 2, 2),
    (9, 'Легковые', 'cars', 2, 2),
    (10, 'Запчасти', 'parts', 2, 2),
    
    -- Для "Услуг"
    (11, 'Ремонт', 'repair', 3, 2),
    (12, 'Обслуживание', 'maintenance', 3, 2),
    
    -- 3 уровень (конкретные виды)
    -- Для мясной продукции
    (13, 'Говядина', 'beef', 5, 3),
    (14, 'Свинина', 'pork', 5, 3),
    (15, 'Птица', 'poultry', 5, 3),
    
    -- Для запчастей
    (16, 'Двигатель', 'engine', 10, 3),
    (17, 'Тормоза', 'brakes', 10, 3),
    
    -- Для ремонта
    (18, 'Ремонт двигателя', 'engine_repair', 11, 3),
    (19, 'Кузовной ремонт', 'body_repair', 11, 3)
    """)

    # Организации
    op.execute("""
    INSERT INTO organizations (id, name, building_id) VALUES
    (1, 'ООО "Рога и Копыта"', 2),
    (2, 'Мясной Двор', 1),
    (3, 'Молочные Реки', 1),
    (4, 'АвтоГруз', 3),
    (5, 'ЛегкоАвто', 3),
    (6, 'Фермерские Овощи', 4),
    (7, 'ДвигательСервис', 5),
    (8, 'Кузовной Центр', 5)
    """)

    # Телефоны
    op.execute("""
    INSERT INTO phones (id, number, organization_id) VALUES
    (1, '2-222-222', 1),
    (2, '3-333-333', 1),
    (3, '8-923-666-13-13', 1),
    (4, '8-495-111-22-33', 2),
    (5, '8-495-444-55-66', 3),
    (6, '8-812-777-88-99', 4),
    (7, '8-812-123-45-67', 5),
    (8, '8-843-555-11-22', 6),
    (9, '8-862-333-44-55', 7),
    (10, '8-862-987-65-43', 8)
    """)

    # Связи организаций с видами деятельности
    op.execute("""
    INSERT INTO organization_activity (organization_id, activity_id) VALUES
    -- ООО "Рога и Копыта" (разные виды)
    (1, 2), (1, 10), (1, 16),
    
    -- Мясной Двор (вся мясная иерархия)
    (2, 5), (2, 13), (2, 14),
    
    -- Молочные Реки
    (3, 6),
    
    -- АвтоГруз
    (4, 8),
    
    -- ЛегкоАвто
    (5, 9), (5, 17),
    
    -- Фермерские Овощи
    (6, 7),
    
    -- ДвигательСервис
    (7, 18),
    
    -- Кузовной Центр
    (8, 19)
    """)


def downgrade():
    op.execute("DELETE FROM organization_activity")
    op.execute("DELETE FROM phones")
    op.execute("DELETE FROM organizations")
    op.execute("DELETE FROM activities")
    op.execute("DELETE FROM buildings")
