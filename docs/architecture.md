# System Architecture

## Database Architecture

    user_management
        user_profile
            users
                user_id                                     UUID 7
                username                                    String(32)
                first_name                                  String(25)
                middle_name                                 String(25)
                last_name                                   String(25)
                date_of_birth                               Date
                gender                                      [male, female, other]
                username_updated_at                         Datetime with timezone
                created_at                                  Datetime with timezone
                updated_at                                  Datetime with timezone
                deleted_at                                  Datetime with timezone
                status                                      [active, inactive, ]
            email_addresses
                email_address_id                            UUID 7
                user_id                                     UUID 7
                email_address                               EmailStr
                is_verified                                 Boolean
                created_at                                  Datetime with timezone
                updated_at                                  Datetime with timezone
                deleted_at                                  Datetime with timezone
                status                                      [active, inactive, ]
        auth
            invalidated_refresh_tokens
                invalidated_refresh_token_id                UUID 7
                user_id                                     UUID 7
                hashed_refresh_token                        String
                expires_at
                created_at                                  Datetime with timezone
                updated_at                                  Datetime with timezone
                deleted_at                                  Datetime with timezone
                status                                      [active, inactive, ]
            credentials
                credential_id                               UUID 7
                user_id                                     UUID 7
                hashed_password                             String
                created_at                                  Datetime with timezone
                updated_at                                  Datetime with timezone
                deleted_at                                  Datetime with timezone
                status                                      [active, inactive, ]
            password_histories
                password_history_id                         UUID
                user_id                                     UUID
                hashed_password                             String
                created_at                                  Datetime with timezone
                updated_at                                  Datetime with timezone