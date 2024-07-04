import pandas as pd
import re
from google.cloud import bigquery
from google.oauth2 import service_account


class Projects:
    """ Třída, která načítá a reprezentuje tabulku projektů.
    Funguje pouze v rámci Google Colab prostředí.

    :param projects: DataFrame načtených dat ze zdroje pravdy nebo z nově vytvořené (vyfiltrované) instance
    :type projects: DataFrame
    :param summary_cfp: DataFrame s agregovanými údaji na úrovni veřejných soutěží
    :type summary_cfp: DataFrame
    :param summary_prog: DataFrame s agregovanými údaji na úrovni programů
    :type summary_prog: DataFrame
    """

    def __init__(self, df: object = None):
        """ Kontstruktor, který načte data do DataFrame a vytvoří agregovanou tabulku.
        """
        if df is None:
            self.projects = self._get_projects()
        else:
            self.projects = df
        self.summary_cfp = self.create_summary()
        self.summary_prog = self.create_summary('prog')

    def _get_projects(self) -> pd.DataFrame:
        """ Načte data o projektech z databáze zdroje pravdy v Bigquery.
           Lze použít pouze v rámci Google Colab prostředí.


       :return: DataFrame načtených dat
       """
        credentials = service_account.Credentials.from_service_account_file(
            '/content/drive/Shareddrives/Analytické oddělení/Data/Zdrojová data/data-poc-424211-81ef80050634.json')
        project_id = 'data-poc-424211'
        client = bigquery.Client(credentials=credentials, project=project_id)

        query = """
        SELECT *
        FROM `data-poc-424211.ssot_test.projekty_ssot`
        """
        df = client.query(query).to_dataframe()
        return df

    def create_summary(self, level: str = 'cfp') -> pd.DataFrame:
        """ Vytvoří agregovaný souhrn buď na úrovni veřejných soutěží (defaultní) nebo na úrovni programů.


       :param level: určuje, na jaké úrovni se provede agregace
                   * 'cfp' (defaultní) - na úrovni veřejných soutěží
                   * 'prog' - na úrovni programů
       :return: agregovaný DataFrame, který obsahuje:
                   * Počet podaných projektů
                   * Počet podpořených projektů
                   * Náklady podpořených projektů
                   * Podpora podpořených projektů
       """
        if level not in ['cfp', 'prog']:
            raise ValueError('Neexistující forma agregace.')

        temp_df = self.projects.copy()
        temp_df['Podpořené'] = temp_df.apply(
            lambda x: 'Ano' if x['faze_projektu'] in ['Realizace', 'Implementace', 'Ukončené'] else 'Ne', axis=1)
        submitted = temp_df.groupby(['kod_programu', 'kod_VS']).agg(
            {'projectcode': 'count', 'naklady_celkem': 'sum', 'podpora_celkem': 'sum'}).reset_index()
        funded = temp_df[temp_df['Podpořené'] == 'Ano'].groupby(['kod_programu', 'kod_VS']).agg(
            {'projectcode': 'count', 'naklady_celkem': 'sum', 'podpora_celkem': 'sum'}).reset_index()

        summary_df = pd.merge(submitted[['kod_programu', 'kod_VS', 'projectcode']], funded, how='inner',
                              on=['kod_programu', 'kod_VS'])
        summary_df.columns = ['kod_programu', 'kod_VS', 'Podané', 'Podpořené', 'Náklady', 'Podpora']

        if level == 'cfp':
            pass
        elif level == 'prog':
            summary_df = summary_df.groupby('kod_programu').agg('sum', numeric_only=True).reset_index()

        return summary_df

    def select_programme(self, *args: str) -> 'Projects':
        """ Vyfiltruje dataframe projektů tak, aby obsahovala pouze projekty vybraných programů.


       :param args: kódy programů (dvoumístné - například 'FW'), které se mají vyfiltrovat
       :return: nová instance třídy Projects s vyfiltrovanými údaji
       :raise: ValueError
       """

        existing_programmes = self.projects['kod_programu'].unique()

        missing_programmes = [prog for prog in args if prog not in existing_programmes]

        if missing_programmes:
            raise ValueError(f'Programy {missing_programmes} neexistují.')


        else:
            programme_list = [prog for prog in args]
            select_df = self.projects[self.projects['kod_programu'].isin(programme_list)].reset_index(drop=True)
            return Projects(select_df)

    def select_cfp(self, *args: str) -> 'Projects':
        """ Vyfiltruje dataframe projektů tak, aby obsahovala pouze projekty vybraných veřejných soutěží.


       :param args: kódy veřejných soutěží (čtyřmístné - například 'FW01'), které se mají vyfiltrovat
       :return: nová instance třídy Projects s vyfiltrovanými údaji
       :raise: ValueError
       """
        existing_cfp = self.projects['kod_VS'].unique()

        missing_cfp = [cfp for cfp in args if cfp not in existing_cfp]

        if missing_cfp:
            raise ValueError(f'Veřejné soutěže {missing_cfp} neexistují.')


        else:
            cfp_list = [cfp for cfp in args]
            select_df = self.projects[self.projects['kod_VS'].isin(cfp_list)].reset_index(drop=True)
            return Projects(select_df)

    def select_funded(self) -> 'Projects':
        """ Vyfiltruje dataframe projektů tak, aby obsahoval pouze podpořené projekty.


       :return: nová instance třídy Projects s vyfiltrovanými údaji
       """
        funded_states = ['Realizace', 'Implementace', 'Ukončené']
        select_df = self.projects[self.projects['faze_projektu'].isin(funded_states)].reset_index(drop=True)
        return Projects(select_df)

    def select_cep(self, level: int, *args: str) -> 'Projects':

        """ Vyfiltruje tabulku tak, aby obsahovala pouze projekty vybraných oborů nebo skupin oborů klasifikace CEP

        :param level: úroveň - 1 = skupiny oborů CEP, 2 = obory CEP
        :param args: kódy skupin oborů CEP (1 písmeno) nebo oborů CEP (2 písmena), které se mají vyfiltrovat
              úroveň 1 - skupiny oborů:
                               * A	= A - Společenské vědy
                               * B	= B - Fyzika a matematika
                               * C	= C - Chemie
                               * D	= D - Vědy o zemi
                               * E	= E - Biovědy
                               * F	= F - Lékařské vědy
                               * G	= G - Zemědělství
                               * I	= I - Informatika
                               * J	= J - Průmysl
                               * K	= K - Vojenství a politika
              úroveň 2 - obory CEP dostupná zde https://docs.google.com/spreadsheets/d/1VknMmHAjKspJmyYlCeJCVEOn01xFGETbTNKi4dMvqf8/edit#gid=0

        :return: nová instance třídy Projects s vyfiltrovanými údaji
        :raise: ValueError
        """
        if level == 1:
            incorrect_level = [lvl for lvl in args if len(lvl) != 1]
            if incorrect_level:
                raise ValueError("Pro úroveň 1 (Skupina oborů CEP) je nutné zvolit pouze jednopísmenný kód!")
            else:
                cep1_enum = ["A", "B", "C", "D", "E", "F", "G", "I", "J", "K"]
                incorrect_cep1 = [cep1 for cep1 in args if cep1 not in cep1_enum]
                if incorrect_cep1:
                    raise ValueError(f"Skupina oborů CEP {incorrect_cep1} není v číselníku skupin oborů CEP!")
                else:
                    existing_cep1 = self.projects['CEP1'].str[:1].unique()
                    missing_cep1 = [cep1 for cep1 in args if cep1 not in existing_cep1]
                    if missing_cep1:
                        raise ValueError(
                            f"Žádný projekt ze skupiny oborů CEP {missing_cep1} není v zadaném výběru nebo v této skupině oborů vůbec nebyl v TA ČR žádný projekt podpořen.")
                    else:
                        cep1_list = [cep1 for cep1 in args]
                        select_df = self.projects[self.projects['CEP1'].str[:1].isin(cep1_list)].reset_index(drop=True)
                        return Projects(select_df)
        elif level == 2:
            incorrect_level = [lvl for lvl in args if len(lvl) != 2]
            if incorrect_level:
                raise ValueError("Pro úroveň 2 (Obory CEP) je nutné zvolit pouze dvoupísmenný kód!")
            else:
                cep2_enum = [
                    'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ'
                    , 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO'
                    , 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI'
                    , 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DO'
                    , 'EA', 'EB', 'EC', 'ED', 'EE', 'EF', 'EG', 'EH', 'EI'
                    , 'FA', 'FB', 'FC', 'FD', 'FE', 'FF', 'FG', 'FH', 'FI', 'FJ', 'FK', 'FL', 'FM', 'FN', 'FO', 'FP',
                    'FQ', 'FR', 'FS'
                    , 'GA', 'GB', 'GC', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GJ', 'GK', 'GL', 'GM'
                    , 'IN'
                    , 'JA', 'JB', 'JC', 'JD', 'JE', 'JF', 'JG', 'JH', 'JI', 'JJ', 'JK', 'JL', 'JM', 'JN', 'JO', 'JP',
                    'JQ', 'JR', 'JS', 'JT', 'JU', 'JV', 'JW', 'JY'
                    , 'KA']
                incorrect_cep2 = [cep2 for cep2 in args if cep2 not in cep2_enum]
                if incorrect_cep2:
                    raise ValueError(f"Obor {incorrect_cep2} není v číselníku oborů CEP!")
                else:
                    existing_cep2 = self.projects['CEP1'].str[:2].unique()
                    missing_cep2 = [cep2 for cep2 in args if cep2 not in existing_cep2]
                    if missing_cep2:
                        raise ValueError(
                            f"Žádný projekt s oborem CEP {missing_cep2} není v zadaném výběru nebo s tímto oborem vůbec nebyl v TA ČR žádný projekt podpořen.")
                    else:
                        cep2_list = [cep2 for cep2 in args]
                        select_df = self.projects[self.projects['CEP1'].str[:2].isin(cep2_list)].reset_index(drop=True)
                        return Projects(select_df)
        else:
            raise ValueError("Lze zvolit pouze úroveň 1 nebo 2")

    def select_ford(self, level, *args: str) -> 'Projects':
        """ Vyfiltruje tabulku tak, aby obsahovala pouze projekty vybraných oborů nebo
        skupin oborů klasifikace FORD

        :param level: úroveň - 1 = Vědní oblast, 2 = FIELDS OF RESEARCH AND DEVELOPMENT (FORD), 3 = DETAILED FORD
        :param args: kódy úrovní oborů FORD (1,2 nebo 3-písmenný), které se mají vyfiltrovat
              úroveň 1 - skupiny oborů
                        * 1	= 1. Natural Sciences
                        * 2	= 2. Engineering and Technology
                        * 3	= 3. Medical and Health Sciences
                        * 4	= 4. Agricultural and veterinary sciences
                        * 5	= 5. Social Sciences
                        * 6 = 6. Humanities and the Arts
              podrobně rozepsaná úroveň 2 (FIELDS OF RESEARCH AND DEVELOPMENT (FORD))
              a úroveň 3 (DETAILED FORD) jsou dostupnézde https://docs.google.com/spreadsheets/d/1J5OChOGxdTZGXOAMeU0icp5Kiz88BhSndRbxJ94A0nc/edit#gid=0
        :return: nová instance třídy Projects s vyfiltrovanými údaji
        :raise: ValueError
         """
        self.projects["ford_code"] = self.projects["ford1"].apply(
            lambda text: re.search(r'\b(\d{5})\b', text).group(1) if isinstance(text, str) and text and re.search(
                r'\b(\d{5})\b', text) else None)

        if level == 1:
            incorrect_level = [lvl for lvl in args if len(lvl) != 1]
            if incorrect_level:
                raise ValueError("Pro úroveň 1 (Vědní oblast) je nutné zvolit pouze jednočíselný kód!")
            else:
                ford1_enum = ['1', '2', '3', '4', '5', '6']
                incorrect_ford1 = [ford1 for ford1 in args if ford1 not in ford1_enum]
                if incorrect_ford1:
                    raise ValueError(f"Vědní oblast FORD {incorrect_ford1} není v číselníku FORD!")
                else:
                    existing_ford1 = self.projects['ford_code'].str[:1].unique()
                    missing_ford1 = [ford1 for ford1 in args if ford1 not in existing_ford1]
                    if missing_ford1:
                        raise ValueError(
                            f"Žádný projekt z Vědního oboru FORD {missing_ford1} není v zadaném výběru nebo vůbec nebyl v TA ČR žádný takový projekt podpořen.")
                    else:
                        ford1_list = [ford1 for ford1 in args]
                        select_df = self.projects[self.projects['ford_code'].str[:1].isin(ford1_list)].reset_index(
                            drop=True)
                        return Projects(select_df)

        elif level == 2:
            incorrect_level = [lvl for lvl in args if len(lvl) != 3]
            if incorrect_level:
                raise ValueError(
                    "Pro úroveň 2 (FIELDS OF RESEARCH AND DEVELOPMENT (FORD)) je nutné zvolit pouze trojčíselný kód!")
            else:
                ford2_enum = ['101', '102', '103', '104', '105', '106', '107'
                    , '201', '202', '203', '204', '205', '206', '207', '208', '209', '210', '211'
                    , '301', '302', '303', '304', '305'
                    , '401', '402', '403', '404', '405'
                    , '501', '502', '503', '504', '505', '506', '507', '508', '509'
                    , '601', '602', '603', '604', '605']
                incorrect_ford2 = [ford2 for ford2 in args if ford2 not in ford2_enum]
                if incorrect_ford2:
                    raise ValueError(f"Obor {incorrect_ford2} není v číselníku oborů FORD!")
                else:
                    existing_ford2 = self.projects['ford_code'].str[:3].unique()
                    missing_ford2 = [ford2 for ford2 in args if ford2 not in existing_ford2]
                    if missing_ford2:
                        raise ValueError(
                            f"Žádný projekt s oborem FORD {missing_ford2} není v zadaném výběru nebo s tímto oborem vůbec nebyl v TA ČR žádný projekt podpořen.")
                    else:
                        ford2_list = [ford2 for ford2 in args]
                        select_df = self.projects[self.projects['ford_code'].str[:3].isin(ford2_list)].reset_index(
                            drop=True)
                        return Projects(select_df)

        elif level == 3:
            incorrect_level = [lvl for lvl in args if len(lvl) != 5]
            if incorrect_level:
                raise ValueError("Pro úroveň 3 (DETAILED FORD) je nutné zvolit pouze pětičíselný kód!")
            else:
                ford3_enum = ['10101', '10102', '10103', '10201', '10301', '10302', '10303', '10304', '10305', '10306',
                              '10307', '10308', '10401', '10402', '10403', '10404', '10405', '10406', '10501', '10502',
                              '10503', '10504', '10505', '10506', '10507', '10508', '10509', '10510', '10511', '10601',
                              '10602', '10603', '10604', '10605', '10606', '10607', '10608', '10609', '10610', '10611',
                              '10612', '10613', '10614', '10615', '10616', '10617', '10618', '10619', '10620'
                    , '20101', '20102', '20103', '20104', '20201', '20202', '20203', '20204', '20205', '20206', '20301',
                              '20302', '20303', '20304', '20305', '20306', '20401', '20402', '20501', '20502', '20503',
                              '20504', '20505', '20506', '20601', '20602', '20701', '20702', '20703', '20704', '20705',
                              '20706', '20707', '20801', '20802', '20803', '20901', '20902', '20903', '21001', '21002',
                              '21101'
                    , '30101', '30102', '30103', '30104', '30105', '30106', '30107', '30108', '30109', '30201', '30202',
                              '30203', '30204', '30205', '30206', '30207', '30208', '30209', '30210', '30211', '30212',
                              '30213', '30214', '30215', '30216', '30217', '30218', '30219', '30220', '30221', '30223',
                              '30224', '30225', '30226', '30227', '30229', '30230', '30301', '30302', '30303', '30304',
                              '30305', '30306', '30307', '30308', '30309', '30310', '30311', '30312', '30401', '30402',
                              '30403', '30404', '30405', '30501', '30502'
                    , '40101', '40102', '40103', '40104', '40105', '40106', '40201', '40202', '40203', '40301', '40401',
                              '40402', '40403'
                    , '50101', '50102', '50103', '50201', '50202', '50203', '50204', '50205', '50206', '50301', '50302',
                              '50401', '50402', '50403', '50404', '50501', '50502', '50601', '50602', '50603', '50701',
                              '50702', '50703', '50704', '50801', '50802', '50803', '50804', '50901', '50902'
                    , '60101', '60102', '60201', '60202', '60203', '60204', '60205', '60206', '60301', '60302', '60303',
                              '60304', '60401', '60402', '60403', '60404', '60405', '60501']
                incorrect_ford3 = [ford3 for ford3 in args if ford3 not in ford3_enum]
                if incorrect_ford3:
                    raise ValueError(f"Obor {incorrect_ford3} není v číselníku oborů CEP!")
                else:
                    existing_ford3 = self.projects['ford_code'].str[:5].unique()
                    missing_ford3 = [ford3 for ford3 in args if ford3 not in existing_ford3]
                    if missing_ford3:
                        raise ValueError(
                            f"Žádný projekt s oborem FORD {missing_ford3} není v zadaném výběru nebo s tímto oborem vůbec nebyl v TA ČR žádný projekt podpořen.")
                    else:
                        ford3_list = [ford3 for ford3 in args]
                        select_df = self.projects[self.projects['ford_code'].str[:5].isin(ford3_list)].reset_index(
                            drop=True)
                        return Projects(select_df)

        else:
            raise ValueError("Lze zvolit pouze úroveň 1,2 nebo 3")


class Organizations:
    """ Třída, která načítá a reprezentuje tabulku organizací.

    Funguje pouze v rámci Google Colab prostředí.

    :param organizations: DataFrame načtených dat ze zdroje nebo z nově vytvořené (vyfiltrované) instance
    :type organizations: DataFrame
    :param summary_cfp: DataFrame s agregovanými údaji na úrovni veřejných soutěží
    :type summary_cfp: DataFrame
    :param summary_prog: DataFrame s agregovanými údaji na úrovni programů
    :type summary_prog: DataFrame
    :param summary_ico: DataFrame s agregovanými údaji na úrovni organizací
    :type summary_ico: DataFrame
    """

    def __init__(self, df: object = None):
        """ Kontstruktor, který načte data do DataFrame, očistí finanční hodnoty a vytvoří agregovanou tabulku.

        :param df: dataframe instance Project
        """
        if df is None:
            self.organizations = self._get_organizations()
            self._data_preparing()
        else:
            self.organizations = df

        self.summary_cfp = self.create_summary()
        self.summary_prog = self.create_summary('prog')
        self.summary_ico = self.create_summary('ico')

    def _get_organizations(self) -> pd.DataFrame:
        """ Načte data o organizacích ze "zdroje pravdy" z databázového úložiště BigQuery.
        Lze použít pouze v rámci Google Colab prostředí.

        :return: DataFrame načtených dat ze zdroje
        """

        credentials = service_account.Credentials.from_service_account_file(
            '/content/drive/Shareddrives/Analytické oddělení/Data/Zdrojová data/data-poc-424211-81ef80050634.json')
        project_id = 'data-poc-424211'
        client = bigquery.Client(credentials=credentials, project=project_id)

        query = """
        SELECT *
        FROM `data-poc-424211.ssot_test.organizace_ssot`
        """
        df = client.query(query).to_dataframe()
        return df

    def _data_preparing(self):
        """ Interní funkce, která doplní potřebná data, které nejsou ve zdroji pravdy v tabulce organizací.
        """
        self.organizations["kod_program"] = self.organizations["projectcode"].str[:2]
        if ["Kód programu"] == 'TG':
            self.organizations["kod_vs"] = self.organizations["projectcode"].str[:6]
        else:
            self.organizations["kod_vs"] = self.organizations["projectcode"].str[:4]
        self.organizations["typeorg_kod"] = self.organizations["typ_organizace"].str[:2]

        map_roles = {"Příjemce": "HP", "Hlavní příjemce": "HP", "Zahraniční partner": "ZU", "Další účastník": "DU"}
        self.organizations["role_kod"] = self.organizations["role"].map(map_roles)

        map_kraj = {"Hlavní město Praha": "PH", "Středočeský kraj": "ST", "Ústecký kraj": "US", "Liberecký kraj": "LI",
                    "Pardubický kraj": "PA", "Královéhradecký kraj": "KR", "Karlovarský kraj": "KA",
                    "Plzeňský kraj": "PL",
                    "Jihočeský kraj": "JC", "Kraj Vysočina": "VY", "Jihomoravský kraj": "JM", "Zlínský kraj": "ZL",
                    "Olomoucký kraj": "OL", "Moravskoslezský kraj": "MO", "ZAH": "ZP"}
        self.organizations["kraj_kod"] = self.organizations["kraj"].map(map_kraj)

        credentials = service_account.Credentials.from_service_account_file(
            '/content/drive/Shareddrives/Analytické oddělení/Data/Zdrojová data/data-poc-424211-81ef80050634.json')
        project_id = 'data-poc-424211'
        client = bigquery.Client(credentials=credentials, project=project_id)

        query = """
        SELECT *
        FROM `data-poc-424211.ssot_test.projekty_ssot`
        """
        projekty_df = client.query(query).to_dataframe()
        self.organizations = pd.merge(self.organizations,
                                      projekty_df[["projectcode", "faze_projektu", "stav_projektu"]], on='projectcode',
                                      how="left")

    def create_summary(self, level: str = 'cfp') -> pd.DataFrame:
        """ Vytvoří agregovaný souhrn buď na úrovni veřejných soutěží (defaultní),na úrovni programů
        nebo organizací.

        :param level: určuje, na jaké úrovni se provede agregace
                      * 'cfp' (defaultní) - na úrovni veřejných soutěží
                      * 'prog' - na úrovni programů
                      # 'ico' - na úrovni jednotlivých organizací
        :return: agregovaný DataFrame, který obsahuje:
                * Počet žádostí o podporu
                * Počet účastí v podpořených projektech
                * Náklady organizace/organizací v podpořených projektech
                * Podpora organizace/organizací v podpořených projektech
        """
        if level not in ['cfp', 'prog', 'ico']:
            raise ValueError('Neexistující forma agregace.')

        temp_df = self.organizations.copy()
        temp_df['Podpořené'] = temp_df.apply(
            lambda x: 'Ano' if x['faze_projektu'] in ['Realizace', 'Implementace', 'Ukončené'] else 'Ne', axis=1)

        if level == 'ico':
            submitted = temp_df.groupby('ICO_organizace').agg({'projectcode': 'nunique'}).reset_index()
            funded = temp_df[temp_df['Podpořené'] == 'Ano'].groupby('ICO_organizace').agg(
                {'projectcode': 'nunique', 'naklady_celkem': 'sum', 'podpora_celkem': 'sum'}).reset_index()

            summary_df = pd.merge(submitted, funded, how='left', on='ICO_organizace',
                                  suffixes=('_podane', '_podporene'))
            summary_df.rename(columns={'projectcode_podane': 'Podané', 'projectcode_podporene': 'Podpořené'},
                              inplace=True)
            summary_df.fillna(0, inplace=True)
            summary_df['Podpořené'] = summary_df['Podpořené'].astype(int)
            summary_df = summary_df.sort_values('podpora_celkem', ascending=False).reset_index(drop=True)

            return summary_df

        else:
            submitted = temp_df.groupby(['kod_program', 'kod_vs']).agg(
                {'ICO_organizace': 'count', 'naklady_celkem': 'sum', 'podpora_celkem': 'sum'}).reset_index()
            funded = temp_df[temp_df['Podpořené'] == 'Ano'].groupby(['kod_program', 'kod_vs']).agg(
                {'ICO_organizace': 'count', 'naklady_celkem': 'sum', 'podpora_celkem': 'sum'}).reset_index()

            summary_df = pd.merge(submitted[['kod_program', 'kod_vs', 'ICO_organizace']], funded, how='inner',
                                  on=['kod_program', 'kod_vs'])
            summary_df.columns = ['kod_program', 'kod_vs', 'Podané', 'Podpořené', 'Náklady', 'Podpora']

            if level == 'prog':
                summary_df = summary_df.groupby('kod_program').agg('sum', numeric_only=True).reset_index()

            return summary_df

    def select_ico(self, *args: str) -> 'Organizations':
        """ Vyfiltruje tabulku tak, aby obsahovala pouze konkrétní vybrané organizace na základě zadaného IČ.

        :param args: IČ organizace/organizací, které se mají vyfiltrovat
        :return: nová instance třídy Organizations s vyfiltrovanými údaji
        :raise: ValueError
        """

        existing_ico = self.organizations['ICO_organizace'].unique()

        missing_ico = [ico for ico in args if ico not in existing_ico]

        if missing_ico:
            raise ValueError(f'Organizace {missing_ico} neexistuje/neexistují.')

        else:
            ico_list = [ico for ico in args]
            select_df = self.organizations[self.organizations['ICO_organizace'].isin(ico_list)].reset_index(drop=True)
            return Organizations(select_df)

    def select_programme(self, *args: str) -> 'Organizations':
        """ Vyfiltruje tabulku tak, aby obsahovala pouze organizace z vybraných programů.

        :param args: kódy programů, které se mají vyfiltrovat
        :return: nová instance třídy Organizations s vyfiltrovanými údaji
        :raise: ValueError
        """

        existing_programmes = self.organizations['kod_program'].unique()

        missing_programmes = [prog for prog in args if prog not in existing_programmes]

        if missing_programmes:
            raise ValueError(f'Programy {missing_programmes} neexistují.')

        else:
            programme_list = [prog for prog in args]
            select_df = self.organizations[self.organizations['kod_program'].isin(programme_list)].reset_index(
                drop=True)
            return Organizations(select_df)  # todo maybe another class Programms?

    def select_cfp(self, *args: str) -> 'Organizations':
        """ Vyfiltruje tabulku tak, aby obsahovala pouze organizace z vybraných veřejných soutěží.

        :param args: kódy veřejných soutěží, které se mají vyfiltrovat
        :return: nová instance třídy Organizations s vyfiltrovanými údaji
        :raise: ValueError
        """
        existing_cfp = self.organizations['kod_vs'].unique()

        missing_cfp = [cfp for cfp in args if cfp not in existing_cfp]

        if missing_cfp:
            raise ValueError(f'Veřejné soutěže {missing_cfp} neexistují.')

        else:
            cfp_list = [cfp for cfp in args]
            select_df = self.organizations[self.organizations['kod_vs'].isin(cfp_list)].reset_index(drop=True)
            return Organizations(select_df)

    def select_funded(self) -> 'Organizations':
        """ Vyfiltruje tabulku tak, aby obsahovala pouze organizace v podpořených projektech.

        :return: nová instance třídy Organizations s vyfiltrovanými údaji
        """
        funded_states = ['Realizace', 'Implementace', 'Ukončené']
        select_df = self.organizations[self.organizations['faze_projektu'].isin(funded_states)].reset_index(drop=True)
        return Organizations(select_df)

    def select_type(self, *args: str) -> 'Organizations':
        """ Vyfiltruje tabulku tak, aby obsahovala pouze organiazce podle vybraného typu organizace.

        :param args: kódy typu organizací, které se mají vyfiltrovat
                    * UP = mikro podnik
                    * MP = malý podnik
                    * SP = střední podnik
                    * VP = velký podnik
                    * VO = výzkumná organizace
                    * DPO = další právnické osoby veřejného i soukromého práva
                    * O = ostatní uchazeči povolení ZD
        :return: nová instance třídy Organizations s vyfiltrovanými údaji
        :raise: ValueError
        """

        existing_orgtype = self.organizations['typeorg_kod'].unique()

        missing_orgtype = [orgtype for orgtype in args if orgtype not in existing_orgtype]

        if missing_orgtype:
            raise ValueError(f'Typy organizace {missing_orgtype} neexistují.')

        else:
            orgtype_list = [orgtype for orgtype in args]
            select_df = self.organizations[self.organizations['typeorg_kod'].isin(orgtype_list)].reset_index(drop=True)
            return Organizations(select_df)

    def select_role(self, *args: str) -> 'Organizations':
        """ Vyfiltruje tabulku tak, aby obsahovala pouze organiazce podle vybraného typu role.

        :param args: kódy rolí, které se mají vyfiltrovat
                    * HP = hlavní příjemce
                    * DU = další účastník
                    * ZU = zahraniční účastník
        :return: nová instance třídy Organizations s vyfiltrovanými údaji
        :raise: ValueError
        """

        existing_orgtype = self.organizations['role_kod'].unique()

        missing_orgtype = [orgtype for orgtype in args if orgtype not in existing_orgtype]

        if missing_orgtype:
            raise ValueError(f'Typy organizace {missing_orgtype} neexistují.')

        else:
            orgtype_list = [orgtype for orgtype in args]
            select_df = self.organizations[self.organizations['role_kod'].isin(orgtype_list)].reset_index(drop=True)
            return Organizations(select_df)

    def select_region(self, *args: str) -> 'Organizations':
        """ Vyfiltruje tabulku tak, aby obsahovala pouze organiazce podle vybraného kraje.

        :param args: kódy krajů, které se mají vyfiltrovat
                    * PH = Hlavní město Praha
                    * ST = Středočeský kraj
                    * US = Ústecký kraj
                    * LI = Liberecký kraj
                    * PA = Pardubický kraj
                    * KR = Královéhradecký kraj
                    * KA = Karlovarský kraj
                    * PL = Plzeňský kraj
                    * JC = Jihočeský kraj
                    * VY = Kraj Vysočina
                    * JM = Jihomoravský kraj
                    * ZL = Zlínský kraj
                    * OL = Olomoucký kraj
                    * MO = Moravskoslezský kraj
                    * ZP = ZAH
        :return: nová instance třídy Organizations s vyfiltrovanými údaji
        :raise: ValueError
        """

        existing_orgtype = self.organizations['kraj_kod'].unique()

        missing_orgtype = [orgtype for orgtype in args if orgtype not in existing_orgtype]

        if missing_orgtype:
            raise ValueError(f'Typy organizace {missing_orgtype} neexistují.')

        else:
            orgtype_list = [orgtype for orgtype in args]
            select_df = self.organizations[self.organizations['kraj_kod'].isin(orgtype_list)].reset_index(drop=True)
            return Organizations(select_df)


def projects_finance() -> pd.DataFrame:
    """ Načte data o financích projektů z databáze zdroje pravdy v Bigquery.
    Finance jsou v rozdělení po jednotlivých letech.
    Lze použít pouze v rámci Google Colab prostředí.

    :return: DataFrame načtených dat ze zdroje
    """
    credentials = service_account.Credentials.from_service_account_file(
        '/content/drive/Shareddrives/Analytické oddělení/Data/Zdrojová data/data-poc-424211-81ef80050634.json')
    project_id = 'data-poc-424211'
    client = bigquery.Client(credentials=credentials, project=project_id)

    query = """
           SELECT *
           FROM `data-poc-424211.ssot_test.projekty_finance_ssot`
           """
    df = client.query(query).to_dataframe()
    return df


def organizations_finance() -> pd.DataFrame:
    """ Načte data o financích organizací z databáze zdroje pravdy v Bigquery.
    Finance jsou v rozdělení po jednotlivých letech.
    Lze použít pouze v rámci Google Colab prostředí.

    :return: DataFrame načtených dat ze zdroje
    """
    credentials = service_account.Credentials.from_service_account_file(
        '/content/drive/Shareddrives/Analytické oddělení/Data/Zdrojová data/data-poc-424211-81ef80050634.json')
    project_id = 'data-poc-424211'
    client = bigquery.Client(credentials=credentials, project=project_id)

    query = """
           SELECT *
           FROM `data-poc-424211.ssot_test.organizace_finance_ssot`
           """
    df = client.query(query).to_dataframe()
    return df


def results() -> pd.DataFrame:
    """ Načte data o výsledcích projektů z databáze zdroje pravdy v Bigquery.
    Lze použít pouze v rámci Google Colab prostředí.

    :return: DataFrame načtených dat ze zdroje
    """
    credentials = service_account.Credentials.from_service_account_file(
        '/content/drive/Shareddrives/Analytické oddělení/Data/Zdrojová data/data-poc-424211-81ef80050634.json')
    project_id = 'data-poc-424211'
    client = bigquery.Client(credentials=credentials, project=project_id)

    query = """
               SELECT *
               FROM `data-poc-424211.ssot_test.vysledky_ssot`
               """
    df = client.query(query).to_dataframe()
    return df


def cfp() -> pd.DataFrame:
    """ Načte data o veřejných soutěží z databáze zdroje pravdy v Bigquery.
    Lze použít pouze v rámci Google Colab prostředí.

    :return: DataFrame načtených dat ze zdroje
    """
    credentials = service_account.Credentials.from_service_account_file(
        '/content/drive/Shareddrives/Analytické oddělení/Data/Zdrojová data/data-poc-424211-81ef80050634.json')
    project_id = 'data-poc-424211'
    client = bigquery.Client(credentials=credentials, project=project_id)

    query = """
                   SELECT *
                   FROM `data-poc-424211.ssot_test.VS_ssot`
                   """
    df = client.query(query).to_dataframe()
    return df
