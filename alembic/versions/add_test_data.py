"""add_test_data"""

from alembic import op

# revision identifiers
revision = 'add_test_data'
down_revision = 'create_tables'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    INSERT INTO buildings (id, address, latitude, longitude) VALUES
    (1, 'г. Москва, ул. Ленина 1, офис 3', 55.7558, 37.6173),
    (2, 'г. Москва, ул. Блюхера 32/1', 55.7625, 37.6163),
    (3, 'г. Санкт-Петербург, Невский пр. 28', 59.9343, 30.3351)
    """)
    
    op.execute("""
    INSERT INTO activities (id, name, category, parent_id, level) VALUES
    (1, 'Еда', 'food', NULL, 1),
    (2, 'Мясная продукция', 'meat', 1, 2),
    (3, 'Молочная продукция', 'dairy', 1, 2),
    (4, 'Автомобили', 'auto', NULL, 1),
    (5, 'Грузовые', 'trucks', 4, 2),
    (6, 'Легковые', 'cars', 4, 2),
    (7, 'Запчасти', 'parts', 4, 2),
    (8, 'Аксессуары', 'accessories', 7, 3)
    """)

    op.execute("""
    INSERT INTO organizations (id, name, building_id) VALUES
    (1, 'ООО "Рога и Копыта"', 2),
    (2, 'Мясной Двор', 1),
    (3, 'Молочные Реки', 1),
    (4, 'АвтоГруз', 3),
    (5, 'ЛегкоАвто', 3)
    """)

    op.execute("""
    INSERT INTO phones (id, number, organization_id) VALUES
    (1, '2-222-222', 1),
    (2, '3-333-333', 1),
    (3, '8-923-666-13-13', 1),
    (4, '8-495-111-22-33', 2),
    (5, '8-495-444-55-66', 3),
    (6, '8-812-777-88-99', 4),
    (7, '8-812-123-45-67', 5)
    """)

    op.execute("""
    INSERT INTO organization_activity (organization_id, activity_id) VALUES
    (1, 4), (1, 7),
    (2, 2),
    (3, 3),
    (4, 5),
    (5, 6), (5, 8)
    """)


def downgrade():
    op.execute("DELETE FROM organization_activity")
    op.execute("DELETE FROM phones")
    op.execute("DELETE FROM organizations")
    op.execute("DELETE FROM activities")
    op.execute("DELETE FROM buildings")