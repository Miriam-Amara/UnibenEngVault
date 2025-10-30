function Header({ menu, role }){
    return(
        <header>
            <div>
                {menu}
            </div>
            <h3>
                UnibenEngVault
            </h3>
            <div>
                {role}
            </div>
        </header>
    );
}

export default Header