import streamlit as st
import base64
import requests
from phone import capture_camera, get_exchange_rates, convert_currency


def fetch_currencies():
    url = 'https://openexchangerates.org/api/currencies.json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json() 
    else:
        st.error("Failed to fetch currency data.")
        return {}


navbar_style = """
    <style>
    /* The sidebar menu */
    .sidebar {
        height: 100%; /* Full-height */
        width: 250px; /* Width of the sidebar */
        position: fixed; /* Stay in place */
        z-index: 1; /* Stay on top */
        top: 0;
        left: 0;
        background-color: #111; /* Black background color */
        overflow-x: hidden; /* Disable horizontal scroll */
        transition: 0.5s; /* Transition effect to slide in the sidebar */
        padding-top: 60px; /* Padding at the top */
        display: none; /* Initially hide the sidebar */
    }

    /* Sidebar links */
    .sidebar a {
        padding: 10px 15px;
        text-decoration: none;
        font-size: 25px;
        color: white;
        display: block;
        transition: 0.3s;
    }

    /* When hovered, change color */
    .sidebar a:hover {
        color: #f1f1f1;
    }

    /* The button to open the sidebar */
    .openbtn {
        font-size: 20px;
        cursor: pointer;
        background-color: #111;
        color: white;
        padding: 10px 15px;
        border: none;
        position: fixed;
        top: 80px; /* Adjust the top position */
        left: 15px;
        z-index: 2; /* Ensures the button is above other content */
    }

    .openbtn:hover {
        background-color: #444;
    }

    /* Show sidebar */
    .show-sidebar {
        display: block; /* Show the sidebar when this class is added */
    }

    /* CSS to position the currency dropdowns */
    .currency-dropdown {
        position: fixed;
        top: 20px; /* Distance from the top */
        right: 20px; /* Distance from the right */
        z-index: 3; /* Ensure it's above other content */
        background-color: rgba(0, 0, 0, 0.7); /* Semi-transparent background */
        padding: 10px; /* Padding for better appearance */
        border-radius: 8px; /* Rounded corners */
        color: white; /* White text color */
    }
    </style>
"""



def show_home(currencies):
    st.title("")  
    
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background-color: #100c08; /* Set a black background */
            color: #FFF; /* Set text color to white */
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown(
        "<h1 style='text-align: center; font-size:70px;'>Convertly</h1>", 
        unsafe_allow_html=True
    ) 
    
    st.markdown(
        "<h3 style='text-align: center; font-size:25px; margin-bottom: 2px; padding-bottom: 2px; line-height: 1;'>Travel, Snap, Exchange</h3>", 
        unsafe_allow_html=True
    )  

    st.markdown(
        "<h3 style='text-align: center; font-size:20px; font-style: italic; margin-top: 0px; padding-top: 0px; line-height: 1;'>Your Gateway to Effortless Currency Conversion</h3>", 
        unsafe_allow_html=True
    )


    file_ = open("plan2.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()


    st.markdown(
        f'''
        <div style="display: flex; justify-content: center; margin-bottom: 0;">
            <img src="data:image/gif;base64,{data_url}" alt="gif" width="500">
        </div>
        ''',
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 0px !important;
            padding-bottom: 0px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(navbar_style, unsafe_allow_html=True)
    st.markdown("""
        <div id="mySidebar" class="sidebar">
            <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
            <a href="#" onclick="document.querySelector('button[data-testid=stButton]').click()">Manual</a>
            <a href="#" onclick="document.querySelectorAll('button[data-testid=stButton]')[1].click()">Camera</a>
        </div>

        <button class="openbtn" onclick="openNav()">☰</button>

        <script>
        function openNav() {
            document.getElementById("mySidebar").classList.add('show-sidebar'); // Show the sidebar
        }

        function closeNav() {
            document.getElementById("mySidebar").classList.remove('show-sidebar'); // Hide sidebar
        }
        </script>
    """, unsafe_allow_html=True)


    st.markdown('<div style="position: fixed; top: 20px; right: 20px; z-index: 3;" class="currency-dropdown">', unsafe_allow_html=True)


    col1, col2, col4, col5= st.columns([0.5, 1, 1, 0.5]) 

    with col2:
        base_currency = st.selectbox("From", list(currencies.keys()), index=0)

    with col4:
        target_currency = st.selectbox("To", list(currencies.keys()), index=1)

    st.session_state['base_currency'] = base_currency
    st.session_state['target_currency'] = target_currency

    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col4, col5 = st.columns([0.5, 1, 1, 0.5]) 


    button_style = """
    <style>
    .stButton>button {
        font-size: 18px;
        padding: 12px 24px;
        width: 100%;
        border-radius: 8px;
        margin-bottom: 20px; /* Adds gap between the buttons */
        border: 2px solid white; /* White outline */
        background-color: transparent; /* Transparent background */
        color: white; /* White text color */
        transition: all 0.3s ease; /* Smooth transition for all properties */
    }
    """
    st.markdown(button_style, unsafe_allow_html=True)

    with col2:
        if st.button("Manual"):
            st.session_state.page = "Page 1" 
            st.rerun() 

    with col4:
        if st.button("Camera"):
            st.session_state.page = "Page 2" 
            st.rerun() 


def fetch_exchange_rates(base_currency):
    url = f'https://openexchangerates.org/api/latest.json?app_id=cae1121bb98743a592755e21f4acc039&base={base_currency}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['rates'] 
    else:
        st.error("Failed to fetch exchange rates.")
        return {}


def show_page1():
    converted_amount = 0
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background-color: #100c08; /* Set a black background */
            color: #FFF; /* Set text color to white */
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(
        "<h1 style='text-align: center; font-size:50px;'>Currency Conversion</h1>", 
        unsafe_allow_html=True
    )  

    st.markdown('<div style="position: fixed; top: 20px; right: 20px; z-index: 3;" class="currency-dropdown">', unsafe_allow_html=True)

    st.markdown("Enter Amount and Select Currency")
    
    col1, col2 = st.columns([2, 1]) 

    with col1:
        #base_amount = st.text_input("Amount", value="0.00", key="base_amount")
        base_amount = st.text_input("Amount", value="0.00", key="base_amount")

    with col2:
        base_currency = st.selectbox("From", st.session_state.get('base_currency', None))
        #base_currency = st.session_state.get('base_currency', None)
    
    #st.markdown('</div>', unsafe_allow_html=True) 


    col3, col4 = st.columns([2, 1])

    with col4:
        target_currency = st.selectbox("To", st.session_state.get('target_currency', None))
        #target_currency = st.session_state.get('target_currency', None)

    st.markdown('</div>', unsafe_allow_html=True)  # Close the dropdown div


    #exchange_rates = fetch_exchange_rates(base_currency)
    rates = get_exchange_rates()
       
    if st.button("Convert"):
        try:
            amount = float(base_amount) 
            converted_amount = convert_currency(amount, base_currency, target_currency, rates)
            if converted_amount is None:
                st.error("Conversion failed. Please check the currencies.")
        except ValueError:
            st.error("Please enter a valid amount.")
    
    
    
    with col3:
        #target_amount = st.text_input("Amount", value="0.00", key="target_amount")
        target_amount = st.text_input("Converted Amount", value=round(converted_amount,2), disabled=True)


    if st.button("Back to Home"):
        st.session_state.page = "Home" 
        st.rerun()  


def show_page2():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background-color: #100c08; /* Set a black background */
            color: #FFF; /* Set text color to white */
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown(
        "<h1 style='text-align: center; font-size:40px;'>Currency Conversion via Camera</h1>", 
        unsafe_allow_html=True
    ) 
    

    st.markdown(
        "<h3 style='text-align: center; font-size:20px; margin-bottom: 2px; padding-bottom: 2px; line-height: 1;'>Click the button to scan the price using your camera.</h3>", 
        unsafe_allow_html=True
    )  
    

    if st.button("Scan Price"):
        amount = capture_camera()
        if amount:
            st.session_state.captured_amount = float(amount)
            st.success(f"Captured Amount: ${amount}")
        else:
            st.error("Failed to capture any amount from the camera.")


    base_currency = st.session_state.get('base_currency', None)
    target_currency = st.session_state.get('target_currency', None)
    

    #if 'captured_amount' in st.session_state:
        #st.write(f"Captured Amount: ${st.session_state.captured_amount}")
    if base_currency and target_currency:
        st.write(f"Converting from **{base_currency}** to **{target_currency}**.")

        rates = get_exchange_rates()
        #if rates:
            #base_currency = st.selectbox("From", list(rates.keys()), index=0)
            #target_currency = st.selectbox("To", list(rates.keys()), index=1)
            
        if st.button("Convert"):
            amount = st.session_state.captured_amount
            converted_amount = convert_currency(amount, base_currency, target_currency, rates)
            if converted_amount is not None:
                st.success(f"{amount} {base_currency} is equal to {converted_amount:.2f} {target_currency}")
            else:
                st.error("Conversion failed. Please check the currencies.")
        
    if st.button("Back to Home"):
        st.session_state.page = "Home" 
        st.rerun()  



if 'page' not in st.session_state:
    st.session_state.page = "Home" 

currencies = fetch_currencies()


if st.session_state.page == "Home":
    show_home(currencies)
elif st.session_state.page == "Page 1":
    show_page1()
elif st.session_state.page == "Page 2":
    show_page2()
