from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.domain.models.models import User
from app.utils.database.session import get_db
from app.utils.database.database import Base, engine
from app.domain.schemas.user import UserCreate, UserUpdate
from app.domain.services.security import get_password_hash, verify_password, create_access_token, secret_key
from datetime import timedelta

router = APIRouter()
oauth2_scheme= OAuth2PasswordBearer("/users/login")

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms="HS256")
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user



@router.post("/users/create_superadmin")
async def create_superadmin(user:UserCreate,db: Session=Depends(get_db)):
    userbd = db.query(User).filter(User.role == "superadmin").first()
    if userbd:
        raise HTTPException(status_code=401, detail="There can only be one superadmin", headers={"WWW-Authenticate": "Bearer"})
    else:
        if (user.role=="manager" or user.role=="customer"):
            raise HTTPException(status_code=401, detail="Role can only be customer", headers={"WWW-Authenticate": "Bearer"})
        else:
            password_hashed=get_password_hash(user.password)
            db_user=User(
                username=user.username,
                email=user.email,
                hashed_password=password_hashed,
                role=user.role,
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        

@router.post("/users/managers")
async def create_manager(user:UserCreate, current_user: User = Depends(get_current_user),db:Session=Depends(get_db)):
    if current_user.role=="superadmin":
        if (user.role=="customer" or user.role=="superadmin"):
            raise HTTPException(status_code=401, detail="Role can only be manager", headers={"WWW-Authenticate": "Bearer"})
        else:
            password_hashed=get_password_hash(user.password)
            db_user=User(
                username=user.username,
                email=user.email,
                hashed_password=password_hashed,
                role=user.role,
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
    else:
        raise HTTPException(status_code=401, detail="Managers can only be registered by Superadmin", headers={"WWW-Authenticate": "Bearer"})

@router.get("/users/managers")
async def get_manager(current_user: User = Depends(get_current_user),db:Session=Depends(get_db)):
    if current_user.role=="superadmin":
        user = db.query(User).filter(User.role == "manager").first()
        return user
    else:
        raise HTTPException(status_code=401, detail="Managers can only be accessed by Superadmin", headers={"WWW-Authenticate": "Bearer"})

@router.put("/users/managers/{manager_id}")
async def update_manager(manager_id: str, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "superadmin":
        raise HTTPException(status_code=403, detail="Not enough permissions", headers={"WWW-Authenticate": "Bearer"})

    manager = db.query(User).filter(User.id == manager_id).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    
    if user_update.role == "superadmin":
        raise HTTPException(status_code=400, detail="Superadmin role cannot be modified. Update allowed for manager or client roles only.")
    for key, value in user_update.dict(exclude_unset=True).items():
        if key == "password":
            hashed_password = get_password_hash(value)
            setattr(manager, "hashed_password", hashed_password)
        else:
            setattr(manager, key, value)

    db.commit()
    db.refresh(manager)
    return manager

@router.delete("/user/managers/{manager_id}")
def delete_manager(manager_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "superadmin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    manager = db.query(User).filter(User.id == manager_id).first()
    if not manager:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Manager not found")
    if manager.role!="manager":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The ID you want to delete must belong to a manager")
    db.delete(manager)
    db.commit()
    return manager

@router.get("/users")
async def get_users(db:Session=Depends(get_db)):
    data=db.query(User).all()
    user_names = []  
    for user in data:
        user_names.append(user.username)  
        # O para imprimir directamente:
        print(f"Nombre de usuario: {user.username}")
        print(f"Correo de usuario: {user.email}")
    print(user_names) 
    return data

@router.post("/users/register")
async def createUser(user:UserCreate,db: Session=Depends(get_db)):
    if (user.role=="manager" or user.role=="superadmin"):
         raise HTTPException(status_code=401, detail="Role can only be customer", headers={"WWW-Authenticate": "Bearer"})
    else:
        password_hashed=get_password_hash(user.password)
        db_user=User(
            username=user.username,
            email=user.email,
            hashed_password=password_hashed,
            role=user.role,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

@router.get("/users/me")
async def user(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/users/{user_id}")
async def update_user(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role != "customer":
        raise HTTPException(status_code=400, detail="Only customers can be modified")

    if current_user.role== "manager":
        raise HTTPException(status_code=400, detail="Only customers and superadmin can modify")
    
    if user_update.role != "customer":
        raise HTTPException(status_code=400, detail="Role can only be customer")
        
    for key, value in user_update.dict(exclude_unset=True).items():
        if key == "password":
            hashed_password = get_password_hash(value)
            setattr(user, "hashed_password", hashed_password)
        else:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@router.post("/users/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires= timedelta(minutes=30)
    access_token_jwt=create_access_token({"sub":user.username},access_token_expires)
    return {
        "access_token": access_token_jwt, 
        "token_type": "bearer"
    }

